
'''
Created on Nov 2, 2018

@author: css-redhat

'''

import random
import time
import datetime
from openshift import config
from ocp_app_mgmt import OcpAppMgmt
from glusto.core import Glusto as g
from ocp_exceptions import ExecutionError

# TODO: Convert all the "oc" shell commands to use OpenShift python client
# TODO: THere are ~11 functions to be converted and validated.
# TODO: Add proper doc strings to the libs if not added.


class FluentdOperations(OcpAppMgmt):
    def __init__(self, config_file=None):
        self.first_master = g.config['first_master']
        self.namespace = g.config['ocp_logging_project_name']
        OcpAppMgmt.__init__(self, config_file=None)

    def fluentd_can_deploy_all_nodes(self, namespace=None):

        """Check that Fluentd can deploy on all nodes in a namespace:
           The logging project should have an empty node selector to ensure
           Fluentd can deploy on all nodes
        :param: namespace
        :returns: boolean True or False
        """
        # Get a list of all the nodes
        lst_proj_res = []
        lst_proj_res = super(FluentdOperations, self).list_project()
        for x in lst_proj_res:
            if (x.metadata.name == "openshift-logging"):
                node_sel = x.metadata.annotations['openshift.io/node-selector']
        if node_sel == "":
            g.log.info("Fluentd cannot deploy on all nodes.")
            _test_fld_deploy = True
        else:
            _test_fld_deploy = False
        return _test_fld_deploy

    # Check that  fluentd is not falling behind journald/json-file and stabilizing

    def check_fluentd_not_falling_behind(self):

        """ Check if fluentd is falling behind journald
            On Compute node running the centos-logtest pod, monitor journald
            message rate from logtest and the backlog of fluentd,
            how far behind it is behind journald by number of messages:

            Make sure that the second value is not increasing over time
            and stabilizing

            Example:
            # journalctl -S "$( date +'%Y-%m-%d %H:%M:%S'
            --date="60 seconds ago" )" | wc -l; journalctl
            -c $( cat /var/log/journal.pos ) | wc -l

            Sample Results:
                     32471
                     630
        """
        cmd_journal = "journalctl --since '60 seconds ago' | wc -l"
        cmd_fluent = "journalctl -c $( cat /var/log/journal.pos ) | wc -l"
        fld_score = 0
        prev_fltd_rate = 0
        # Over a period of time check that Fluentd is not falling behind
        t_start = datetime.datetime.now()
        t_end = t_start + datetime.timedelta(minutes=1)
        while t_start < t_end:
            for i in range(10):
                ret, journal_rate, err = g.run(self.first_master, cmd_journal)
                g.log.info("Journal is logging at the rate of ", journal_rate)
                ret, fluentd_rate, err = g.run(self.first_master, cmd_fluent)
                g.log.info("Sleeping for 5 secs")
                fluentd_rate = int(float(fluentd_rate))
                time.sleep(5)
                if fluentd_rate <= prev_fltd_rate:
                    fld_score += 1
                    prev_fltd_rate = fluentd_rate
                    t_start = datetime.datetime.now()
                else:
                    prev_fltd_rate = fluentd_rate
                    t_start = datetime.datetime.now()
        # if the final tally is too low (less than 3) flag as Fluentd lagging
        if fld_score <= 3:
            g.log.info("LOW SCORE : Fluentd is falling behind.")
            return False
        else:
            g.log.info("Fluentd is keeping up with Journal logs")
            return True


class ElasticOperations(OcpAppMgmt):
    def __init__(self, first_master, ocp_logging_project_name,
                 config_file=None):
        self.first_master = first_master
        self.ocp_logging_project_name = ocp_logging_project_name
        self.kube_config_file = config_file
        if config_file:
            OcpAppMgmt.__init__(self, config_file=self.kube_config_file)

    def get_top_elastic_indexes(self):

        """
        Command:
        curl -kv -H "Authorization: Bearer `oc whoami -t`"
        https://`oc get svc logging-kibana -n openshift-logging
        -o jsonpath='{.spec.clusterIP}'`/elasticsearch/.all/_search?sort
        =@timestamp:desc | python -m json.tool | tee timestamp_logs.txt
        :parameters: namespace
        :returns: tuple list of top 10 indexes
        """
        pass

    def get_elasticsearch_indexes_state(self):
        """ Get state of the elastic search

        :return: dict where podname is the key and value is list of
            state of indexes seen from each pod
            For example:
                {'logging-es-data-master-mz7182ko-2-drhts': ['green'],
                'logging-es-data-master-cypn0g0h-2-9kpzb': ['green'],
                'logging-es-data-master-6lmw4rub-2-pxl4j': ['green']}
        :raises: ocp_exceptions.ExecutionError in case of execution
            failures.
        """
        g.log.info("Getting elasticsearch indexes state...")

        # Get elastic search pods
        cmd = (("oc get pods -n %s -l component=es -o "
                "jsonpath='{.items[*].metadata.name}'") %
               self.ocp_logging_project_name)
        ret, out, err = g.run(self.first_master, cmd)
        if ret == 0 and out:
            _out = list(out.split())
            elasticsearch_pods = filter(None, _out)
        else:
            raise ExecutionError("Failed to get elastic search pods: %s" %
                                 err)

        # Get elastic seatch indexes states
        elasticsearch_pods_indexes_state_dict = {}
        for elasticsearch_pod in elasticsearch_pods:
            cmd = ("oc exec %s -n %s -- curl -s -k "
                   "--cert /etc/elasticsearch/secret/admin-cert "
                   "--key /etc/elasticsearch/secret/admin-key "
                   "https://logging-es:9200/_cat/indices?v | "
                   "awk '{if(NR>1)print}' | awk '{print $1}'" %
                   (elasticsearch_pod, self.ocp_logging_project_name))
            ret, out, err = g.run(self.first_master, cmd)
            elasticsearch_pods_indexes_state_dict[elasticsearch_pod] = None
            if out:
                _out = list(set(out.split("\n")))
                elasticsearch_pods_indexes_state_dict_value = (list(filter(None, _out)))
                if ('green' in elasticsearch_pods_indexes_state_dict_value or
                        'yellow' in elasticsearch_pods_indexes_state_dict_value or
                        'red' in elasticsearch_pods_indexes_state_dict_value):
                    elasticsearch_pods_indexes_state_dict[elasticsearch_pod] = (
                        elasticsearch_pods_indexes_state_dict_value
                    )

        g.log.info("Elasticsearch pods indexes state:\n%s",
                   elasticsearch_pods_indexes_state_dict)
        return elasticsearch_pods_indexes_state_dict

    def are_elasticsearch_pods_indexes_green(self):
        """ Check if elasticsearch pods indexes green

        :return: bool. True if all indexes of elasticsearch pods are green.
            False otherwise.
        :raises: ocp_exceptions.ExecutionError in case of execution failures.
        """

        try:
            elasticsearch_pods_indexes_state_dict = \
                self.get_elasticsearch_indexes_state()
        except ExecutionError as e:
            raise ExecutionError(e.message)

        _rc = True
        for pod in elasticsearch_pods_indexes_state_dict:
            elasticsearch_pod_indexes_state = (
                elasticsearch_pods_indexes_state_dict[pod])

            if elasticsearch_pod_indexes_state is None:
                _rc = False
            elif not (len(elasticsearch_pod_indexes_state) == 1 and
                      'green' in elasticsearch_pod_indexes_state):
                _rc = False
        return _rc

    def get_elasticsearch_thread_pool_status(self):
        """ Get elasticsearch thread pool status
        :return: dict where podname is the key and the pool status is the value.
            For example:
                {'logging-es-data-master-mz7182ko-2-drhts': {'bulk.queue': '0',
                                                             'bulk.rejected': '0',
                                                             'host': '10.131.2.16',
                                                             'bulk.completed': '1118756',
                                                             'bulk.active': '0',
                                                             'bulk.queueSize': '50'
                                                             },
                 'logging-es-data-master-cypn0g0h-2-9kpzb': {'bulk.queue': '0',
                                                             'bulk.rejected': '0',
                                                             'host': '10.128.2.12',
                                                             'bulk.completed': '729262',
                                                             'bulk.active': '0',
                                                             'bulk.queueSize': '50'
                                                             },
                 'logging-es-data-master-6lmw4rub-2-pxl4j': {'bulk.queue': '0',
                                                             'bulk.rejected': '0',
                                                             'host': '10.128.2.12',
                                                             'bulk.completed': '729262',
                                                             'bulk.active': '0',
                                                             'bulk.queueSize': '50'}
                 }
        :raises: ocp_exceptions.ExecutionErrorn case of execution failures.
        """
        g.log.info("Getting elasticsearch thread pool states...")

        # Get elastic search pods

        obj_ops = OcpLoggingOperations()
        elasticsearch_pods = obj_ops.get_component_pods('es')

        # Get the queues rejected status
        elasticsearch_pods_thread_pool_status = {}
        for elasticsearch_pod in elasticsearch_pods:
            cmd = ("oc exec %s -n %s -- "
                   "curl -s -k --cert /etc/elasticsearch/secret/admin-cert "
                   "--key /etc/elasticsearch/secret/admin-key "
                   "https://localhost:9200/_cat/thread_pool?v\&h="
                   "host,bulk.completed,bulk.rejected,bulk.queue,bulk.active,"
                   "bulk.queueSize" %
                   (elasticsearch_pod, self.ocp_logging_project_name))
            ret, out, err = g.run(self.first_master, cmd)

            elasticsearch_pods_thread_pool_status[elasticsearch_pod] = {}
            if ret == 0 and out:
                _thread_pool_status = list(out.split("\n"))
                thread_pool_status = list(filter(None, _thread_pool_status))
                _fields = list(thread_pool_status[0].split())
                fields = list(filter(None, _fields))
                for each_status in thread_pool_status[1:]:
                    _each_status = list(each_status.split())
                    each_status = list(filter(None, _each_status))
                    for i in range(len(fields)):
                        (elasticsearch_pods_thread_pool_status[elasticsearch_pod][fields[i]]) = each_status[i]
                        g.log.info("Elasticsearch pods thread pool status:\n%s", elasticsearch_pods_thread_pool_status)
        return elasticsearch_pods_thread_pool_status

    def are_elasticsearch_bulk_queues_rejected(self):
        """ Check if elasticseacrh bulk queues are rejected

        :return: bool. True if elasticsearch bluk queues are rejected.
            False otherwise.
        :raises: ocp_exceptions.ExecutionErrorn case of execution failures.
        """
        try:
            elasticsearch_pods_thread_pool_status = \
                self.get_elasticsearch_thread_pool_status()
        except ExecutionError as e:
            raise ExecutionError(e.message)
        _rc = False
        for pod in elasticsearch_pods_thread_pool_status:
            if int(elasticsearch_pods_thread_pool_status[pod]['bulk.rejected']) != 0:
                _rc = True
        return _rc

    def get_elastic_search_dc_info(self, component="es"):
        """ Get elastic search deployment config info
        :param component: component name
        :return: list.
            For example:
                [{'CURRENT': '1', 'DESIRED': '1',
                'NAME': 'logging-es-data-master-6lmw4rub', 'REVISION': '2'},
                 {'CURRENT': '1', 'DESIRED': '1',
                 'NAME': 'logging-es-data-master-cypn0g0h', 'REVISION': '2'},
                 {'CURRENT': '1', 'DESIRED': '1',
                 'NAME': 'logging-es-data-master-mz7182ko', 'REVISION': '2'}]
        :raises: ocp_exceptions.ExecutionErrorn case of execution failures.
        """

        cmd = "oc get dc -n %s " % self.ocp_logging_project_name
        if component:
            cmd = cmd + "--selector=component=%s" % component

        # Get elastic search dc info
        ret, out, err = g.run(self.first_master, cmd)
        if ret != 0:
            raise ExecutionError(
                "Failed to get elastic search dc info for project %s: %s" %
                (self.ocp_logging_project_name, err)
            )

        dc_info_list = []
        if out:
            _out = list(out.split("\n"))
            temp_dc_info_list = list(filter(None, _out))
            _temp_dc_info_list = list(temp_dc_info_list[0].split())
            fields = list(filter(None, _temp_dc_info_list))
            for each_item in temp_dc_info_list[1:]:
                _each_item = list(each_item.split())
                each_item = list(filter(None, _each_item))
                temp_dict = {}
                for i in range(len(each_item)):
                    temp_dict[fields[i]] = each_item[i]
                dc_info_list.append(temp_dict)
        g.log.info("DC info for the project %s:\n%s", self.ocp_logging_project_name,
                   dc_info_list)
        return dc_info_list

    def wait_for_elasticsearch_pods_to_be_online(self, timeout=300):
        """ Wait for elasticseacth pods to be in RUNNING State
            until timeout (default 300 seconds)

        :return: True if elasticsearch pods are in RUNNING state
            within timeout. False otherwise
        :raises: ocp_exceptions.Execution Error in case of execution failures.
        """
        g.log.info("Waiting for elasticsearch pods to be online....")
        counter = 0
        time.sleep(10)
        while counter <= timeout:
            # Get elastic search pods and its state
            cmd = ("oc get pods -n %s -l component=es | "
                   "awk '{if(NR>1)print}' | "
                   "awk '{print $1 , $3}' " % self.ocp_logging_project_name)
            ret, out, err = g.run(self.first_master, cmd)
            if ret == 0 and out:
                elasticsearch_pods_status = filter(None, out.split("\n"))
            else:
                raise ExecutionError("Failed to get elastic search pods info: %s"
                                     % err)
            g.log.info("Elasticsearch pods status:\n%s",
                       elasticsearch_pods_status)

            # Check if pods state are running
            is_running = True
            for elasticsearch_pod_status in elasticsearch_pods_status:
                pod, status = filter(None, elasticsearch_pod_status.split())
                if status:
                    if status.lower() != 'running':
                        is_running = False

            if is_running is False:
                time.sleep(10)
                counter = counter + 10
                continue
            else:
                break
        return is_running

    def restart_elasticsearch_cluster(self):
        """ Restart elasticsearch cluster

        :return: boolean. True if successfully restarted the cluster.
            False otherwise.
        :raises: ocp_exceptions.ExecutionErrorn case of execution failures.
        """

        g.log.info("Restart elasticsearch cluster...")

        # Get elasticsearch deployment configs
        cmd = ("oc get dc -n %s -o=name --selector=component=es" %
               self.ocp_logging_project_name)
        ret, out, err = g.run(self.first_master, cmd)
        if ret == 0 and out:
            _out = list(out.split())
            elasticsearch_deployment_configs = filter(None, _out)
        else:
            raise ExecutionError("Failed to get elastic "
                                 "search deployment configs: %s" % err)

        # Scale down the elasticsearch deployment configs to 0
        for elasticsearch_dc in elasticsearch_deployment_configs:
            cmd = ("oc scale -n %s %s --replicas=0" %
                   (self.ocp_logging_project_name, elasticsearch_dc))
            ret, out, err = g.run(self.first_master, cmd)
            if ret != 0:
                raise ExecutionError(
                    "Failed to scale down elasticsearch deployment config "
                    "'%s' to replica 0" % elasticsearch_dc)
            g.log.info("Successfully scaled down elasticsearch deployment config "
                       "'%s' to replica 0" % elasticsearch_dc)

        # Validate if the elasticsearch deployment configs are scaled down to 0
        try:
            elasticsearch_dc_info = self.get_elastic_search_dc_info()
        except Exception as e:
            raise ExecutionError(e.message)
        _rc = True
        for each_dc_info in elasticsearch_dc_info:
            if int(each_dc_info['CURRENT']) != 0:
                _rc = False
        if _rc is False:
            raise ExecutionError(
                "Failed to validate the replica of deployment config of "
                "project %s is 0" % self.ocp_logging_project_name)
        else:
            g.log.info("Successfully validated the replica of deployment "
                       "config of project %s is 0",
                       self.ocp_logging_project_name)

        # Scale up the elasticsearch deployment configs to 1
        for elasticsearch_dc in elasticsearch_deployment_configs:
            cmd = ("oc scale -n %s %s --replicas=1" %
                   (self.ocp_logging_project_name, elasticsearch_dc))
            ret, out, err = g.run(self.first_master, cmd)
            if ret != 0:
                raise ExecutionError(
                    "Failed to scale up elasticsearch deployment config "
                    "'%s' to replica 1" % elasticsearch_dc)
            g.log.info("Successfully scaled up elasticsearch deployment config "
                       "'%s' to replica 1", elasticsearch_dc)

        # Wait for the pods to get restarted
        is_running = self.wait_for_elasticsearch_pods_to_be_online()
        if is_running is False:
            raise ExecutionError("Elasticsearch pods are not yet "
                                 "in running state even after 5 minutes "
                                 " after scale up")
        else:
            g.log.info("All elasticsearch pods are in running state")

        # Validate if the elasticsearch deployment configs are scaled up to 1
        try:
            elasticsearch_dc_info = self.get_elastic_search_dc_info()
        except Exception as e:
            raise ExecutionError(e.message)
        _rc = True
        for each_dc_info in elasticsearch_dc_info:
            if int(each_dc_info['CURRENT']) != 1:
                _rc = False
        if _rc is False:
            raise ExecutionError(
                "Failed to validate the replica of deployment config of "
                "project %s is 1" % self.ocp_logging_project_name)
        g.log.info("Successfully restarted the elasticsearch cluster")
        return _rc

    def delete_elasticsearch_index(self, delete_all=False):
        """ In case an index is corrupted or simply no longer necessary
            indexes can be deleted

        :param delete_all: True if we want to delete all indexes.
        :return: True if successfully able to delete indexes. False otherwise.
        :raises: ocp_exceptions.ExecutionErrorn case of execution failures.
        """
        # Get elastic search pods
        cmd = (("oc get pods -n %s -l component=es -o "
                "jsonpath='{.items[*].metadata.name}'") %
               self.ocp_logging_project_name)
        ret, out, err = g.run(self.first_master, cmd)
        if ret == 0 and out:
            _out = list(out.split())
            elasticsearch_pods = filter(None, _out)
        else:
            raise ExecutionError("Failed to get elastic search pods: %s" %
                                 err)

        elasticsearch_pod = random.choice(elasticsearch_pods)

        # Delete all indexes
        if delete_all is True:
            cmd = ("oc exec %s -n %s -- curl -s -k "
                   "--cert /etc/elasticsearch/secret/admin-cert "
                   "--key /etc/elasticsearch/secret/admin-key "
                   "-XDELETE https://logging-es:9200/project.svt*" %
                   (elasticsearch_pod, self.ocp_logging_project_name))
            ret, out, err = g.run(self.first_master, cmd)
            if ret != 0:
                raise ExecutionError("Failed to delete all elastic "
                                     "search indexes")
            else:
                if "\"acknowledged\":true" in out:
                    g.log.info("Successfully deleted all the elastic search "
                               "indexes")
                    return True
                else:
                    raise ExecutionError("Failed to delete all elastic "
                                         "search indexes")

        # Get elastic seatch indexes states
        _rc = True
        cmd = ("oc exec %s -n %s -- curl -s -k "
               "--cert /etc/elasticsearch/secret/admin-cert "
               "--key /etc/elasticsearch/secret/admin-key "
               "https://logging-es:9200/_cat/indices?v | "
               "awk '{if(NR>1)print}' | grep -ve '^green' | "
               "awk '{print $1 , $3}'" %
               (elasticsearch_pod, self.ocp_logging_project_name))
        ret, out, err = g.run(self.first_master, cmd)
        if out:
            _out = list(out.split('\n'))
            elasticsearch_pods_indexes_state_value = (
                filter(None, _out))

            g.log.info("Elasticsearch pods indexes state:\n%s",
                       elasticsearch_pods_indexes_state_value)
            for values in elasticsearch_pods_indexes_state_value:
                _values = list(values.split())
                state, index = filter(None, _values)
                if index:
                    cmd = (("oc exec %s -n %s -- curl -s "
                            "--key /etc/elasticsearch/secret/admin-key "
                            "--cert /etc/elasticsearch/secret/admin-cert "
                            "--cacert /etc/elasticsearch/secret/admin-ca "
                            "-XDELETE https://localhost:9200/%s") %
                           (elasticsearch_pod, self.ocp_logging_project_name,
                            index))
                    ret, out, err = g.run(self.first_master, cmd)
                    if ret != 0:
                        g.log.error("Failed to delete index '%s' "
                                    "( state of index is: %s )", index, state)
                        _rc = False
        else:
            g.log.info("All indexes are green. Nothing to delete")
        return _rc


# Generic Operations:
# ------------------


class OcpLoggingOperations(OcpAppMgmt):
    """
    OpenShift Logging Operations Class
    ----------------------------------
    OcpLoggingOps inherits the ocp_app_mgmt as it's super class.

    Contains methods that can be called to perform OpenShift Logging specific
    Operations that can be used in Testing the Logging Use Case.
    - Methods do generic logging operations and validations
    - Methods for Baseline Checks to run after running SVT tool
    - Cleanup methods
    """
    def __init__(self, config_file=None):

        OcpAppMgmt.__init__(self, config_file=None)
        if config_file is None:
            # Load the local config
            config.load_kube_config()
        else:
            # Create a config from a config file
            config.load_kube_config(config_file=str(config_file))
        self.first_master = g.config['first_master']
        self.ocp_user = g.config['ocp_user']
        self.ocp_pass = g.config['ocp_pass']
        self.namespace = g.config['ocp_logging_project_name']
        try:
            cmd = "oc login -u %s -p %s -n %s" % (self.ocp_user, self.ocp_pass, self.namespace)
            ret, out, err = g.run(self.first_master, cmd)
        except:

            raise ExecutionError("Unable to login to the %s Project" % self.namespace)
    # Check that enough memory is configured for each pod and memory utilization is in range

    def check_comp_memory_in_range(self):
        pass

    def check_es_comp_storage_resources_ok(self):
        """
        Check available disk space less than 90% utilization for
                /elasticsearch/persistent
        command:
        for pod in `oc get po -l component=es -o jsonpath='{.items[*].metadata.name}'`;
         do echo $pod; oc exec $pod -- df -h /elasticsearch/persistent; done

        """
        str_es_dir = "/elasticsearch/persistent"
        g.log.info("Checking storage resources in %s for %s" % (self.namespace, str_es_dir))
        lst_pods = self.get_component_pods('es')
        _es_storage_ok = False
        for pod in lst_pods:
            cmd = "oc exec %s -- df -h %s 2> /dev/null | grep %s | awk '{print $5}'" % (pod, str_es_dir, str_es_dir)
            ret, out, err = g.run(self.first_master, cmd)
            if ret != 0:
                    raise ExecutionError("Unable to check elastic pod storage utilization.")
            else:
                # Strip the % form the output
                out = out[:-2]
                if int(out) >= 80:
                    g.log.info("WARNING: Elastic storage is at OVER 80% Utilization")
                    _es_storage_ok = False
                else:
                    g.log.info("Elastic storage is below 80% Utilization")
                    _es_storage_ok = True
            return _es_storage_ok

    def check_errors_in_comp_logs(self):
        """
        Check the Component logs for errors

        :params: String component eg "es", "kibana"
        :returns: Boolean True or False
        """
        pass
    # Check that Components have enough resources and is not constantly restarting

    def check_pods_restarting(self):
        """
        Check that component pods eg fluentd has enough resources and that
        its not constantly restarting.

        Command: oc exec $FLUENTD_POD -- ps -ef

        If the "PID" for fluentd is in the hundreds or thousands after
        a couple of hours or after a few stress tests, the process is
        probably restarting frequently, implying that there is not
        enough memory allocated to the pods.
        :param: component string eg "es", ""fluentd"
        :return: boolean if are restarting: True or and  False if NOT
        """

        dct_comp_str = {"es": 0, "fluentd": 0}

        for key in dct_comp_str:
            # Get list of pods for the key
            lst_comp_pods = self.get_component_pods(key)
            # For each pod in the list check that the PID is less than 100
            for comp_pod in lst_comp_pods:
                cmd_pid = "oc exec %s -- ps -ef 2> /dev/null| grep %s | awk '{print $2}'" % (comp_pod, key)

                ret, out, _ = g.run_local(cmd_pid)

                if ret != 0:
                    raise ExecutionError("Unable to verify if pods are restarting")
                else:
                    if int(float(out)) > 100:
                        # Verify possible memory issue with "oc get pods see if they are restarting alot"
                        cmd = "oc get po | grep %s | awk '{print $4}'" % (key)
                        ret, out, _ = g.run(comp_pod, cmd)
                        if ret == 0 and set(out.split) != 0:
                            dct_comp_str[key] = 1
                        else:
                            pass
        # Fail the test if any have Restarted.

        if 1 in dct_comp_str.values():
            g.log.info("EFK pods are restarting this could be a resource issue.")
            return True
        else:
            g.log.info("Verified EFK pods are NOT continually restarting.")
            return False

    def verify_docker_log_driver_on_ocp_nodes(self, log_driver):
        """
        Method to check if  driver journald or json-file is in use
        on all nodes:
           $ docker info | grep 'Logging Driver'

             Logging Driver: json-file
             :return: dict of log-driver and hostname
        """
        lst_nodes = self.get_cluster_nodes()

        cmd = "docker info 2> /dev/null | grep 'Logging Driver'"
        results = g.run_parallel(lst_nodes, cmd)
        _driver_check = False
        try:
            for key_node, ret_values in results.items():
                return_code, _, _ = ret_values
                _, current_driver, _ = ret_values
                if return_code == 0 and log_driver in current_driver:
                    _driver_check = True
                else:
                    g.log.info("ERROR while trying to verify log driver")
                    _driver_check = False
                    break
        except:

            raise ExecutionError("Exception unable to verify log driver")
        return _driver_check

    def get_component_pods(self, ocp_component):

        """
        Purpose: Create a tuple of pods for the current project/namespace for a
                 singular component.
        CSS-XXX
        List the pods for the specified component
        either: fluentd, es, kibana or curator
         oc get po -l component=fluentd -o jsonpath='{.items[*].metadata.name}'
        :param component  - either fluentd, es, kibana or curator
        :return tuple_component_pods: Returns a list of pods for the specified
        component in the namespace
        """

        try:

            cmd = "oc get po -l component=%s -o \
            jsonpath='{.items[*].metadata.name}'" % (ocp_component)
            _, out, _ = g.run(self.first_master, cmd)
            ls_components = out.split()
        except ExecutionError as e:

            g.log.info("Exception was encountered while trying to obtain \
            OCP %s Pods: %s\n", ocp_component, e)
        return ls_components

    def switch_log_driver(self, log_driver):
        """
        Purpose: To switch to requested log-driver [journald or json-file]
        :param: log_driver to switch to json-file or journald
        :return: Boolean for success or fail
        """
        pass

    def get_journaling_rate_per_min(self):

        """
        Get the journaling rate per min
        """
        pass

    def check_EFK_services_running(self):

        """
        Check EFK services are enabled and running.
        Check Elastic Services
        Check Fluentd Services
        Check Kibana Services
        Check the respective pod status
        :param: self
        :return: True if ALL the pods for each component are RUNNING
                 False if an error occurs or the pod count and number of running pods don't match
        """
        lst_comp_str = {"es", "fluentd", "curator", "kibana"}
        running_score = 0
        pod_count = 0
        # Check that each serice is running state
        for comp in lst_comp_str:
            # Get a list of all the component's pods
            lst_comp_pods = self.get_component_pods(comp)
            pod_count += len(lst_comp_pods)
            # Check that the component pod is in "Running"state
            for comp_pod in lst_comp_pods:
                cmd_comp_state = "oc get po | grep %s | awk '{print $3}'" % (comp_pod)
                ret, out, err = g.run(self.first_master, cmd_comp_state)

                if ret == 0 and 'Running' in out:
                    running_score += 1
                else:
                    raise ExecutionError("Unable to verify if ALL pods are Running")
                    g.log.info("get_service_state method failed : ", err)
                    return False
        if running_score == pod_count:
            return True

    def check_cluster_size_and_types(self):

        """
        Check the number of Masters, Infra and Compute nodes in the cluster

        """
        pass

    def check_haproxy_load_balancer(self):

        """
        Check that HA Proxy load balancer is setup in the cluster.
        """
        pass

    def check_kibana_console(self):

        """"
        P1
        """
        pass

# Basic Checks after Tests
# ------------------------

    def get_cluster_nodes(self):
        """
        Get a list of all the hosts in the cluster.
        :params: object
        :return: a list of nodes
        """
        cmd = "oc get nodes | awk '{print $1}' | grep -ve 'NAME'"
        lst_nodes = []
        ret, out, err = g.run(self.first_master, cmd)
        if out:
            lst_nodes = filter(None, out.split())
        return lst_nodes

    def check_all_nodes_ready(self):

        """
        Check that all nodes in the cluster are in READY state.
        Return True or False
         ***API Returns the string:: "kubelet is posting ready status"
        :return: Boolean True if ALL nodes are READY and False if not
        """
        lst_node_res = []
        # Generate a list of Node Objects
        lst_node_res = super(OcpLoggingOperations, self).list_nodes()
        # Get the Node status Index #4
        nodemsg = [x.status.conditions[4].message for x in lst_node_res.items]
        # Convert the array list to a set and you should only have 1 status
        # if all the nodes are READY there should only be 1 item:

        if len(set(nodemsg)) == 1 and 'kubelet is posting ready status'\
                in nodemsg:
            g.log.info("All the Nodes are in 'READY' state. \n")
            return True
        else:
            g.log.info("ERROR: Not all the Nodes are in 'READY' state. \n")
            return False

    def delete_component_pods(self, component):

        """Delete fluentd pods. Need to use API first
           $ oc delete pods -l component=fluentd
           $ oc delete pods -l component=kibana
           :parameters: component eg 'es', 'kibana', 'fluentd',
           :returns: boolean on successful run or fail
        """
        pass
