import warnings
import time
from kubernetes import client, config
from openshift.dynamic import DynamicClient
from kubernetes.client.rest import ApiException
from subprocess import PIPE, Popen
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from glusto.core import Glusto as g
from urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

'''
Created on Apr 2, 2019

@author: Redhat CSS-QI

'''


class OcpHealthCheck():
    """OpenShift Cluster Health Check Class
    ---------------------------------------
    Purpose: To check overall cluster health.
    
    Usage:
  - To instantiate this class:
    # oc_health = OcpHealthCheck()
       ** You can pass the following parameters to the constructor otherwise the shown default value is used :
            namespace="default", hostname = 'localhost', user='admin', password='redhat'
            to pass a different parameters when instantiating the class:
             oc_health = OcpHealthCheck(namespace="openshift-logging", hostname = 'beaker_host', user='student',\
                   password='Tivoli')
            

  - Each method in this class is a specific health check on the cluster 
     To check the node health of nodes in the cluster :
     
    # test_result = oc_health.check_nodes_health()
    # print test_result
     Each method returns a :boolean: True [PASSED] or False [FAILED] 
    
    """
    def __init__(self, namespace="default", hostname='localhost', user='admin', password='redhat'):
        self.hostname = hostname
        self.namespace = namespace
        self.user = user
        self.password = password
        # Get the token for the host provided "localhost' if none
        try:
            p1 = Popen(["curl", "-sIk",
                        """https://%s:8443/oauth/authorize?response_type=token"""
                        """&client_id=openshift-challenging-client""" % hostname,
                        "--user", "admin:redhat"], stdout=PIPE)
            p2 = Popen(["grep", "-oP", "access_token=\\K[^&]*"], stdin = p1.stdout, stdout = PIPE)
            p1.stdout.close()
        except ApiException as e:
            logger.error("Exception was encountered while trying to obtain a session token: %s\n", e)
        token = p2.communicate()[0]
        self.token = token.strip().decode('ascii')
        self.test_name = "None"
        configuration = client.Configuration()
        configuration.api_key['authorization'] = self.token
        configuration.api_key_prefix['authorization'] = 'Bearer'
        configuration.host = 'https://%s:8443' % self.hostname
        configuration.verify_ssl = False
        k8s_client = client.ApiClient(configuration)
        self.dyn_client = DynamicClient(k8s_client)
        # Get a List of all the known nodes
        try:
            v1_nodes = self.dyn_client.resources.get(api_version='v1', kind='Node')
            node_list = v1_nodes.get()
            self.node_names = [x.metadata.name.encode("ascii") for x in node_list.items]
        except ApiException as e:
            logger.error("Exception was encountered getting a list of Nodes: %s\n", e)
        # List of namespaces/projects
        try:
            v1_projects = self.dyn_client.resources.get(api_version='v1', kind='Project')
            self.namespace_list = v1_projects.get()
        except ApiException as e:
            logger.error("Exception was encountered getting a list of Projects: %s\n", e)

    def check_nodes_health(self):
        """
        Check that all the nodes in the cluster are healthy

        type: OutOfDisk, MemoryPressure, DiskPressure, PIDPressure, Ready

        - have sufficient disk space.
        - All have sufficient memory
        - All Do not have any disk pressure
        - Have a sufficient PIP
        - Are all in ready state
        Return True  if Passed or False if any one of the tests Fail
         ***API Returns the string:: "kubelet has sufficient disk space available" if the space is
                                     sufficient for the node(s)
        :return: Boolean True  if healthy or False if any one of the tests fail
        """
        self.test_name = ' CHECK HEALTH OF NODES : '
        fail_flag = False
        g.log.info("")
        g.log.info(" Test :: %s", self.test_name)
        g.log.info("="*60)
        v1_nodes = self.dyn_client.resources.get(api_version='v1', kind='Node')
        g.log.info("\t Checking Memory, Disk on  all the Nodes.")
        node_list = v1_nodes.get()
        for i in range(4):
            node_states = [x.status.conditions[i].status for x in node_list.items]
            node_states = set(node_states)
            if len(node_states) == 1 and "False" in node_states:
                mode_message = [x.status.conditions[i].message for x in node_list.items]
                mesg = mode_message[0]
                g.log.info( " %d )  %s....... [ PASSED ]" % (i, mesg))
                nodes_healthy = True 
            else:
                g.log.info(" %d )  %s....... [ FAILED ]" % (i, mesg))
                nodes_healthy = False
                fail_flag = True
                break
        # Check the ready state is TRUE
        nodes_ready = [x.status.conditions[4].status for x in node_list.items]
        nodes_ready = set(nodes_ready)
        g.log.info("\t Checking that all the Nodes are in Ready State. ")
        if len(nodes_ready) == 1 and "True" in nodes_ready:
            mode_message = [x.status.conditions[4].message for x in node_list.items]
            mesg = mode_message[0]
            g.log.info(" 4 )   %s....... [ PASSED ]" %  (mesg))
            nodes_healthy = True
        else:
            g.log.info(" 4 )  %s....... [ FAILED ]" % (mesg))
            nodes_healthy = False
            fail_flag = True
        # Lastly verify that you can ssh to the nodes
        retries = 3
        ssh_to_node_ok = {}
        for node in self.node_names:
            ssh_to_node_ok[node] = False
            try_count = 0
            while try_count < retries:
                ret, _, err = g.run(node, "date")
                if ret == 0:
                    ssh_to_node_ok[node] = True
                    g.log.info("Node : %s:    SSH OK: %s", node, ssh_to_node_ok[node])
                    break
                else:
                    ssh_to_node_ok[node] = False
                    g.log.info("Node : %s:    SSH OK: %s", node, ssh_to_node_ok[node])
                    time.sleep(5)
                    fail_flag = True
                    try_count += 1
        if (all(value is True for value in ssh_to_node_ok.values())):
            g.log.info("Connectivity Test....... [ PASSED ]")
        else:
            g.log.info("Connectivity Test....... [ FAILED ]")
        # If the Fail flag catches anything that failed...return False 
        if fail_flag:
            nodes_healthy = False
        return nodes_healthy

    def check_router_registry_health(self, namespace="default"):
        """
        Check Internal Registry and Router
            To check if a router service is running:
            $ oc -n default get deploymentconfigs/router

            The values in the DESIRED and CURRENT columns should match the number of nodes hosts.
            
            Use the same command to check the registry status:
            $ oc -n default get deploymentconfigs/docker-registry

            To verify that all pods are running and on which hosts:
            $ oc -n default get pods -o wide --selector='docker-registry
            :return : a True [PASSED] or False [FAILED] 
            '"""
            
        self.test_name = "CHECK ROUTER AND REGISTRY HEALTH "
        router_reg_health_ok = False
        fail_flag = False
        g.log.info("")
        g.log.info(" Test :: %s", self.test_name)
        g.log.info("="*60)
        v1_depl_config = self.dyn_client.resources.get(api_version='v1', kind='DeploymentConfig')
        depl_configs = v1_depl_config.get()
        lst_comps = ["router", "docker-registry"]
        # Loop 1 check Router health
        # Loop 2: Check internal registry health
        for comp in lst_comps:
            #g.log.info(" Checking ",comp, " Health")
            g.log.info(" Checking %s  Health :", comp)
            desired_repl = [x.status.availableReplicas for x in depl_configs.items \
                            if x.metadata.namespace == namespace and x.metadata.name == comp]
            current_repl = [x.status.readyReplicas for x in depl_configs.items \
                            if x.metadata.namespace == namespace and x.metadata.name == comp]
            repls = [x.status.replicas for x in depl_configs.items 
                    if x.metadata.namespace == namespace and x.metadata.name == comp]
            # Log and display results :
            g.log.info(" - Desired Replicas : %d", desired_repl[0])
            g.log.info(" - Current replicas  : %d", current_repl[0])
            g.log.info(" - Targeted pods    : %d", repls[0])
            
            if desired_repl == current_repl and desired_repl == repls:
                comp_health_ok = True
                g.log.info("%s Health Test....... [ PASSED ]", comp)
            else:
                comp_health_ok = False
                fail_flag = True
                g.log.info("%s Health Test....... [ FAILED ]", comp)
        # If the Failflag catches anything that failed...return False         
        if fail_flag:
            comp_health_ok = False
        return comp_health_ok 
    
    def check_network_connectivity(self, port=8443):
        """
        - Verifying name resolution (Same IP in the following:)
             dig +short docker-registry.default.svc.cluster.local
             oc get svc/docker-registry -n default
        API service and web console
        To verify node host functionality, create a new application. The following example ensures the node
        reaches the docker registry, which is running on an infrastructure node:
         :param: string for the port number used usuallt 443 or 8443 if none use :8443
         :return : Boolean True [PASSED] or False [FAILED] 
        """
        self.test_name = "CHECK NETWORK CONNECTIVITY "
        self.port = port
        network_health_check_ok = False
        fail_flag = False
        g.log.info("") 
        g.log.info(" Test :: %s", self.test_name)
        g.log.info("="*60)
        g.log.info(" Verifying connectivity on master nodes. ")
        g.log.info("    - Verifying name resolution")
        # The output from these two command should have the same IP
        cmd = "dig +short docker-registry.default.svc.cluster.local"
        ret, dig_dns_ip, err = g.run(self.hostname, cmd)
        dig_dns_ip = dig_dns_ip.strip()
        v1_Service = self.dyn_client.resources.get(api_version='v1', kind='Service')
        srvc_list = v1_Service.get()
        oc_dns_ip = [x.spec.clusterIP for x in srvc_list.items 
                    if (x.metadata.namespace == self.namespace and x.metadata.name == "docker-registry")]
        oc_dns_ip = oc_dns_ip[0]
        oc_dns_ip = oc_dns_ip.encode("ascii")
        g.log.info("    - DNS dig output: %s", dig_dns_ip)
        g.log.info("    - OCP API DNS output: %s", oc_dns_ip)
        # Convert from Unicode to String
        if dig_dns_ip == oc_dns_ip :
            network_health_check_ok = True
            g.log.info(" Name resolution test .......[ PASSED ]")
        else:
            fail_flag = True
        # Check #2 :: API service and web console
        g.log.info("Verifying API service and web console. on port 8443 and 443 ")
        cmd = ("curl -k https://%s:%s/healthz" % (self.hostname, self.port))
        ret, ext_client_link_chk, err = g.run(self.hostname, cmd)
         
        if ext_client_link_chk == "ok":
            g.log.info(" Network connectivity test .......[ PASSED ]")
            network_health_check_ok = True
        else:
            g.log.info(" External client link test .......[ FAILED ]")
            fail_flag = True
            network_health_check_ok = False    
        # If the Failflag catches anything that failed...return False
        if fail_flag:
            g.log.info(" Network connectivity test .......[ FAILED ]")
        return network_health_check_ok  

    def check_current_desired_components(self):
        """
        Get a list of projects
        check that for each namespace the desired number of replicas
        oc get dc -n <ocp_logging_project_name> --selector=<component>
         :return : Boolean True [PASSED] or False [FAILED]
        """
        self.test_name = " CHECK FOR DESIRED REPLCAS FOR COMPONENTS: "

    def check_storage(self, min_var_sz=40):
        """STORAGE
            Master instances need at least 40 GB of hard disk space for the /var directory.
            Check the disk usage of a master host using the df command:
             :return : Boolean True [PASSED] or False [FAILED] """ 
        self.test_name = " CHECK STORAGE "  

    def check_api_status(self):
        """API SERVICE STATUS
            The OpenShift API service, atomic-openshift-master-api.service, runs on all master
            instances. To see the status of the service:
            $ systemctl status atomic-openshift-master-api.service
             :return : Boolean True [PASSED] or False [FAILED] """
        self.test_name = "CHECK API SERVICE IS RUNNING "

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
        pass

    def check_ocp_services_running(self):
        pass