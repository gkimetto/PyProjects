#!/usr/bin/python

from openshift import config
from openshift import client as ocpclient
from kubernetes import client as k8sclient
from kubernetes.client.rest import ApiException
from pprint import pformat
import json
from subprocess import PIPE, Popen
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from time import sleep
import logging
import ocp_exceptions

# Initiate child logger. Parent logger is in the script invoking this
# module and is named 'ocp_test_logger'
logger = logging.getLogger('ocp_test_logger.ocp_app_mgmt')

"""
This is a class that provides capabilities to manage resources in an openshift cluster.
The class currently must be present on the master node of the ocp cluster and has a
couple of dependencies.

Dependencies:
  - The openshift python client must be installed. To do so, follow the instructions
    on the github page:
    https://github.com/openshift/openshift-restclient-python
  - Installation of the openshift python client requires that latest version of a
    few packages like python-setuptools. You need to have pip installed to get the latest
    versions of these dependencies. The package name is python-pip.

Usage:
  - To instantiate this class:
    # api_instance = OcpAppMgmt()

  - To create then delete a project:
    # res = api_instance.create_project('myproject')
    # print res
    # api_instance.delete_project('myproject')

  - To create an app from one of the pre-loaded templates in a specific namespace/project:
    # api = api_instance.deploy_template_based_app('myproject', 'httpd-example', 0)
    The above example will create deployment named httpd-example0 in namespace 'myproject'

  - To delete a deployment/app in a namespace/project:
    # api_instance.delete_template_based_app('myproject', 'jenkins-ephemeral', 0)

  - To update the number of replicas to 3 for a deployment/app:
    # api_instance.update_deployment_replicas('myproject', 'httpd-example0', 3)

  - To list pods within a namespace/project:
    # res = api_instance.list_pods_in_a_namespace('myproject')
    # print res

  - To check for readiness of a deployment in a namespace/project:
    # res = api_instance.poll_deployment_readiness_in_a_namespace('myprojects', 'httpd-example0')
    # pprint res
"""

# TODO: Make necessary changes to class to run it from test machine (ansible controller?)
# TODO: There are 28 functions in the class to be validate to run from test machine.
# TODO: Make changes to logger to use g.log or to log to same file.


class OcpAppMgmt(object):
    '''
    This class will enable a user to create and delete apps from the preloaded templates in the openshift master node.
    The create/delete functionality will keep track of the app count in memory via the app_params_dict member of this
    class which contains a count key.
    '''

    def __init__(self, config_file=None):
        # Connect to localhost and use the default k8s config object
        if config_file is None:
            # Load the local config
            config.load_kube_config()
        else:
            # Create a config from a config file
            config.load_kube_config(config_file=str(config_file))
        # constant variable used by the REST calls to return response object in 'pretty' format
        self.pretty = 'pretty_example'
        # All objects in the list value of the 'objects' key of an app template have the same schema and are of the same
        # object type. However, depending on the value of the 'kind' key, different, client type,
        # class and method are to be used for a successful deployment. In order to solve this problem,
        # we create a dictionary that maps these dependencies. We can then use this mapping to dynamically
        # instantiate the right object and call the right method for the kind of deployment we want to make
        self.kind_mapper_dict = {
            'ImageStream':
                {
                    'create':
                        {
                            'client': ocpclient,
                            'class': 'OapiApi',
                            'method': 'create_namespaced_image_stream'
                        },
                    'delete':
                        {
                            'client': ocpclient,
                            'class': 'OapiApi',
                            'method': 'delete_namespaced_image_stream',
                            'body':
                                {
                                    'client': k8sclient,
                                    'model': 'V1DeleteOptions'
                                }
                        }
                },
            'PersistentVolumeClaim':
                {
                    'create':
                        {
                            'client': k8sclient,
                            'class': 'CoreV1Api',
                            'method': 'create_namespaced_persistent_volume_claim'
                        },
                    'delete':
                        {
                            'client': k8sclient,
                            'class': 'CoreV1Api',
                            'method': 'delete_namespaced_persistent_volume_claim',
                            'body':
                                {
                                    'client': k8sclient,
                                    'model': 'V1DeleteOptions'
                                }
                        }
                },
            'Route':
                {
                    'create':
                        {
                            'client': ocpclient,
                            'class': 'OapiApi',
                            'method': 'create_namespaced_route'
                        },
                    'delete':
                        {
                            'client': ocpclient,
                            'class': 'OapiApi',
                            'method': 'delete_namespaced_route',
                            'body':
                                {
                                    'client': k8sclient,
                                    'model': 'V1DeleteOptions'
                                }
                        }
                },
            'DeploymentConfig':
                {
                    'create':
                        {
                            'client': ocpclient,
                            'class': 'OapiApi',
                            'method': 'create_namespaced_deployment_config'
                        },
                    'delete':
                        {
                            'client': ocpclient,
                            'class': 'OapiApi',
                            'method': 'delete_namespaced_deployment_config',
                            'body':
                                {
                                    'client': k8sclient,
                                    'model': 'V1DeleteOptions'
                                }
                        }
                },
            'BuildConfig':
                {
                    'create':
                        {
                            'client': ocpclient,
                            'class': 'OapiApi',
                            'method': 'create_namespaced_build_config'
                        },
                    'delete':
                        {
                            'client': ocpclient,
                            'class': 'OapiApi',
                            'method': 'delete_namespaced_build_config',
                            'body':
                                {
                                    'client': k8sclient,
                                    'model': 'V1DeleteOptions'
                                }
                        }
                },
            'ServiceAccount':
                {
                    'create':
                        {
                            'client': k8sclient,
                            'class': 'CoreV1Api',
                            'method': 'create_namespaced_service_account'
                        },
                    'delete':
                        {
                            'client': k8sclient,
                            'class': 'CoreV1Api',
                            'method': 'delete_namespaced_service_account',
                            'body':
                                {
                                    'client': k8sclient,
                                    'model': 'V1DeleteOptions'
                                }
                        }
                },
            'RoleBinding':
                {
                    'create':
                        {
                            'client': ocpclient,
                            'class': 'OapiApi',
                            'method': 'create_namespaced_role_binding'
                        },
                    'delete':
                        {
                            'client': ocpclient,
                            'class': 'OapiApi',
                            'method': 'delete_namespaced_role_binding',
                            'body':
                                {
                                    'client': k8sclient,
                                    'model': 'V1DeleteOptions'
                                }
                        }
                },
            'Service':
                {
                    'create':
                        {
                            'client': k8sclient,
                            'class': 'CoreV1Api',
                            'method': 'create_namespaced_service'
                        },
                    'delete':
                        {
                            'client': k8sclient,
                            'class': 'CoreV1Api',
                            'method': 'delete_namespaced_service',
                            'body':
                                {
                                    'client': None,
                                    'model': ''
                                }
                        }
                },
            'Secret':
                {
                    'create':
                        {
                            'client': k8sclient,
                            'class': 'CoreV1Api',
                            'method': 'create_namespaced_secret'
                        },
                    'delete':
                        {
                            'client': k8sclient,
                            'class': 'CoreV1Api',
                            'method': 'delete_namespaced_secret',
                            'body':
                                {
                                    'client': k8sclient,
                                    'model': 'V1DeleteOptions'
                                }
                        }
                }
        }
        # This member object contains describes the relevant info needed for creating and deleting apps from a template.
        # The create key references the template variables that need to be changed to ensure unique deployments.
        # The count key is initialized to None and keeps track of app count from 0 to n.
        self.app_params_dict = {
            'jenkins-ephemeral':
                {
                    'create': ('JENKINS_SERVICE_NAME', 'JNLP_SERVICE_NAME')
                },
            'jenkins-persistent':
                {
                    'create': ('JENKINS_SERVICE_NAME', 'JNLP_SERVICE_NAME')
                },
            '128mb-fio':
                {
                    'create': ('NAME')
                },
            'httpd-example':
                {
                    'create': ('NAME')
                },
            'cakephp-mysql-example':
                {
                    'create': ('NAME', 'DATABASE_SERVICE_NAME')
                },
            'dancer-mysql-example':
                {
                    'create': ('NAME', 'DATABASE_SERVICE_NAME')
                },
            'django-psql-example':
                {
                    'create': ('NAME', 'DATABASE_SERVICE_NAME')
                },
            'nodejs-mongodb-example':
                {
                    'create': ('NAME', 'DATABASE_SERVICE_NAME')
                },
            'rails-postgresql-example':
                {
                    'create': ('NAME', 'DATABASE_SERVICE_NAME')
                },
            'cakephp-mysql-persistent':
                {
                    'create': ('NAME', 'DATABASE_SERVICE_NAME')
                },
            'dancer-mysql-persistent':
                {
                    'create': ('NAME', 'DATABASE_SERVICE_NAME')
                },
            'django-psql-persistent':
                {
                    'create': ('NAME', 'DATABASE_SERVICE_NAME')
                },
            'nodejs-mongo-persistent':
                {
                    'create': ('NAME', 'DATABASE_SERVICE_NAME')
                },
            'rails-pgsql-persistent':
                {
                    'create': ('NAME', 'DATABASE_SERVICE_NAME')
                },
            'fio-persistent':
                {
                    'create': ('NAME', 'PVC_NAME')
                }
        }

    def get_auth_token(self):
        """
        Method that returns a session token to be used for REST calls
        using the requests modules
        :return: Authentication token
        """
        try:
            p1 = Popen(["curl", "-sIk",
                        """https://localhost:8443/oauth/authorize?response_type=token"""
                        """&client_id=openshift-challenging-client""",
                        "--user", "admin:redhat"], stdout=PIPE)
            p2 = Popen(["grep", "-oP", "access_token=\\K[^&]*"], stdin=p1.stdout, stdout=PIPE)
            p1.stdout.close()
        except ApiException as e:
            logger.error("Exception was encountered while trying to obtain a session token: %s\n", e)
        token = p2.communicate()[0]
        return token.strip().decode('ascii')

    def get_ocp_version(self):
        """
        Method that returns a list of version components. For example, if oc version
        returns 'v3.10.45', then this function will return ['v3', '10', '45']
        :return: A list of version components
        """
        ocp_version = None
        try:
            process = Popen(['oc', 'version'], stdout=PIPE)
            stdout = process.communicate()
            full_version = [s.strip().decode('ascii') for s in stdout[0].splitlines()][0]
            ocp_version = full_version.split()[1].split(".")
        except ApiException as e:
            logger.error("Exception was encountered while trying to obtain OCP version: %s\n", e)
        return ocp_version

    def get_unprocessed_template(self, template_name):
        """
        The OCP rest client implementation is currently broken
        and an issue has been filed. As a workaround we use
        the requests module to exercise the endpoint to obtain
        an raw app template
        :param template_name: The template name
        :return: A V1Template object on success, None on failure
        """
        token = self.get_auth_token()
        url = 'https://localhost:8443/oapi/v1/namespaces/openshift/templates/' + template_name
        headers = {'Authorization': 'Bearer ' + token}
        # Supress unverified SSL cert warning from response
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = None
        try:
            response = requests.get(url, headers=headers, verify=False)
        except ApiException as e:
            logger.error("Exception was encountered while trying to obtain a template: %s\n", e)

        if response.status_code != 200:
            return None

        return response.json()

    def enumerate_unprocessed_template(self, template, id):
        """
        We use enumerate the minimum required parameters using the
        apps_param_dict 'create' and 'count' fields
        :param template: The json response obj for template get request (as returned by get_unprocessed_template)
        :param id: Unique id of type int
        :return: A json template. If a non-supported template is used,
                 we return None.
        """
        ret = None
        if template is not None:
            app_name = template['metadata']['name']
            if app_name not in self.app_params_dict:
                logger.warning("!!! The app %s is not currently supported, skipping ... !!!", app_name)
            else:
                for obj in template['parameters']:
                    if obj['name'] in self.app_params_dict[app_name]['create']:
                        # Apps that have both ephemeral and persistent versions don't
                        # name their resources differently by default.
                        if 'ephemeral' in app_name:
                            obj['value'] = obj['value'] + '-ephemeral-' + str(id)
                        elif 'persistent' in app_name:
                            obj['value'] = obj['value'] + '-persistent-' + str(id)
                        else:
                            obj['value'] = obj['value'] + '-' + str(id)
                ret = template
        return ret

    def process_enumerated_template(self, template):
        """
        The OCP rest client implementation is currently broken
        and an issue has been filed. As a workaround we use
        the requests module to exercise the endpoint to process
        and app template. In this case, after we enumerate the needed
        deployment parameters
        :param template: The json response obj for template get request (as returned by
            get_unprocessed_template or enumerate_unprocessed_template)
        :return: A processed template of type json on success. None on failure
        """
        response = None
        if template is not None:
            template_dict = json.dumps(template)  # Convert unicode json to python dict
            token = self.get_auth_token()
            url = 'https://localhost:8443/oapi/v1/processedtemplates'
            headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json',
                       'Accept': 'application/json'}
            requests.packages.urllib3.disable_warnings()  # Supress unverified SSL cert warning from response
            try:
                response = requests.post(url, headers=headers, data=template_dict, verify=False)
            except ApiException as e:
                logger.error("Exception was encountered while trying to process a template: %s\n", e)

            if response is not None:
                response_dict = response.json()
                for obj in response_dict['objects']:
                    obj['apiVersion'] = 'v1'
                return response_dict
        return response

    def list_nodes(self):
        """
        Method that returns a list of node objects
        :return: V1NodeList on success. None on failure.
        """
        api_instance = k8sclient.CoreV1Api()
        api_response = None
        try:
            api_response = api_instance.list_node(pretty=self.pretty)
        except ApiException as e:
            logger.error("Exception when calling method list_node: %s\n", e)
        return api_response

    def list_node_memory_cpu_usage(self, node_name):
        """
        Methods that returns the allocated resources section
        from the output of the 'oc describe node <node_name>
        :param node_name: The name of the node to be described
        :return: A list of strings containing the lines of the
                 allocated resources section from the output
                 of the 'oc describe node' command.
                 None on failure.
        """
        allocated_resources = None
        try:
            process = Popen(['oc', 'describe', 'node', node_name], stdout=PIPE)
            stdout = process.communicate()
            res = [s.strip().decode('ascii') for s in stdout[0].splitlines()]
            resources_index = res.index('Allocated resources:')
            allocated_resources = res[resources_index + 2:resources_index + 5]
        except ApiException as e:
            logger.error("Exception was encountered while trying to obtain cpu/mem stats: %s\n", e)
        return allocated_resources

    def deploy_template_based_app(self, domain, template, id):
        """
        This method fetches a raw template by name, enumerates it,
        processes it and uses it to deploy an app in a specified
        domain/project. domain and template params are of type
        string while id is of type int
        :param domain: The domain that will host the app/dc
        :param template: The template to be used to deploy the app/dc
        :param id: Unique id of type int
        :return: The name of the resulting deployment config
        """
        unprocessed_template = self.get_unprocessed_template(template)
        if unprocessed_template is None:
            # skip the deployment for non supported template names
            logger.error("Failed to get the unprocessed template for "
                         "template '%s'. Skipping the deployment for this "
                         "app defined by template '%s'", template, template)
            pass
        else:
            # We enumerate the template using the ident param
            enumerated_unprocessed_template = self.enumerate_unprocessed_template(unprocessed_template, id)

            # If a non supported app was requested, we skip the deployment.
            if enumerated_unprocessed_template is None:
                pass
            else:
                enumerated_processed_template = self.process_enumerated_template(enumerated_unprocessed_template)
                if enumerated_processed_template is None:
                    pass
                else:
                    deployment_names = []
                    # We iterate through the 'objects' key of the template and we deploy each one based on its kind
                    # by dynamically using the appropriate client, class and method.
                    for obj in enumerated_processed_template['objects']:
                        current_obj_type = obj['kind']
                        current_client = self.kind_mapper_dict[current_obj_type]['create']['client']
                        current_class = self.kind_mapper_dict[current_obj_type]['create']['class']
                        current_method = self.kind_mapper_dict[current_obj_type]['create']['method']
                        if current_obj_type == 'DeploymentConfig':
                            deployment_names.append(obj['metadata']['name'])
                        api_instance = getattr(current_client, current_class)()
                        args = (domain, obj)
                        kwargs = {'pretty': self.pretty}
                        try:
                            getattr(api_instance, current_method)(*args, **kwargs)
                        except ApiException as e:
                            logger.error("Exception when calling method %s: %s\n", current_method, e)
                    # TODO: What else should this method return?
                    return deployment_names

    def delete_template_based_app(self, domain, template, id):
        """
        A method to delete a template based app. loops through the objects
        key in the app template and deletes resources bases on their kind.
        :param domain: The namespace containing the targeted app/dc
        :param template: The template corresponding to the targeted app/dc
        :param id: The unique id integer to be appended to the dc name
                   to ensure its uniqueness within a namespace
        :return: None
        """
        unprocessed_template = self.get_unprocessed_template(template)
        if unprocessed_template is None:
            logger.error("Failed to get the unprocessed template for "
                         "template '%s'. Skipping deletion of this app "
                         "defined by template '%s'", template, template)
            pass
        else:
            enumerated_unprocessed_template = self.enumerate_unprocessed_template(unprocessed_template, id)
            enumerated_processed_template = self.process_enumerated_template(enumerated_unprocessed_template)
            for obj in enumerated_processed_template['objects']:
                current_obj_type = obj['kind']
                current_name = obj['metadata']['name']
                current_delete_client = self.kind_mapper_dict[current_obj_type]['delete']['body']['client']
                current_delete_model = self.kind_mapper_dict[current_obj_type]['delete']['body']['model']
                current_client = self.kind_mapper_dict[current_obj_type]['delete']['client']
                current_class = self.kind_mapper_dict[current_obj_type]['delete']['class']
                current_method = self.kind_mapper_dict[current_obj_type]['delete']['method']
                api_instance = getattr(current_client, current_class)()
                if current_delete_client and current_delete_model:
                    body = getattr(current_delete_client, current_delete_model)()
                    args = (current_name, domain, body)
                else:
                    args = (current_name, domain)
                kwargs = {'pretty': self.pretty}
                try:
                    getattr(api_instance, current_method)(*args, **kwargs)
                except ApiException as e:
                    logger.error("Exception when calling method %s: %s\n", current_method, e)

    def create_project(self, project_name, labels=None):
        """
        Method to create a project
        :param project_name: Name of project to be created
        :return: A V1ProjectRequest object on success. None on failure
        """
        api_instance = ocpclient.OapiApi()
        body = ocpclient.V1ProjectRequest()
        body.metadata = k8sclient.V1ObjectMeta(name=project_name)
        api_response = None
        try:
            api_response = api_instance.create_project_request(body,
                                                               pretty=self.pretty)
        except ApiException as e:
            logger.error("Exception when calling method create_project_request: %s\n" % e)
        if labels is not None:
            self.label_project(project_name, labels)
        return api_response

    def label_project(self, project, labels):
        """
        Method that patches a namespace/project with user
        defined labels
        :param project: Name of the project to be patched
        :param labels: An object of type dict(str: str)
        :return: An object of type V1Namespace
        """
        api_instance = k8sclient.CoreV1Api()
        body = {'metadata': {'labels': labels}}
        api_response = None
        try:
            api_response = api_instance.patch_namespace(project, body, pretty=self.pretty)
        except ApiException as e:
            logger.error("Exception when calling method patch_namespace: %s\n" % e)
        return api_response

    def label_deployment_config(self, namespace, dc, labels):
        """
        Method that patches a Deployment Config as a means
        to apply a label to it.
        :param namespace: The name of the namespace containing the targeted dc
        :param dc: The deployment config to be labeled
        :param labels: A dictionary containing the key,val labels
        :return: A V1DeploymentConfig object
        """
        api_instance = ocpclient.OapiApi()
        body = {'metadata': {'labels': labels}}
        api_response = None
        try:
            api_response = api_instance.patch_namespaced_deployment_config(dc,
                                                                           namespace,
                                                                           body,
                                                                           pretty=self.pretty)
        except ApiException as e:
            logger.error("Exception when calling method patch_namespaced_deployment_config: %s\n", e)
        return api_response

    def delete_project(self, project_name):
        """
        Method to delete a project
        :param project_name: The targeted project for deletion
        :return: A V1Status object on success. None on failure
        """
        api_instance = ocpclient.OapiApi()
        api_response = None
        try:
            api_response = api_instance.delete_project(name=project_name,
                                                       pretty=self.pretty)
            logger.debug(pformat(api_response))
        except ApiException as e:
            logger.error("Exception when calling method delete_project: %s\n", e)
        return api_response

    def list_project(self, namespace=None):
        """
        Method to list all or a specific project
        If no parameter is given, it defaults to
        listing all
        :param namespace: Optional parameter specifying
                          the targeted project
        :return: V1Project or a list of V1Project objects, depending on input param.
                 None on failure.
        """
        api_instance = ocpclient.OapiApi()
        project_list = None
        api_response = None
        try:
            project_list = api_instance.list_project()
        except ApiException as e:
            logger.error("Exception when calling method list_project: %s\n", e)

        if project_list is not None:
            if namespace is None:
                api_response = project_list.items
            else:
                for project in project_list.items:
                    if project.metadata.name == namespace:
                        api_response = project
                    else:
                        pass
        return api_response

    def update_deployment_replicas(self, namespace, dc, replicas):
        """
        Method to change number of replicas for a deployment
        :param namespace: The namespace containing the targeted
                          deployment config
        :param dc: The targeted deployment config
        :param replicas: The desired number of replicas
        :return: A V1DeploymentConfig object
        """
        api_instance = ocpclient.OapiApi()
        body = {"spec": {"replicas": replicas}}
        try:
            api_instance.patch_namespaced_deployment_config(dc,
                                                            namespace,
                                                            body,
                                                            pretty=self.pretty)
        except ApiException as e:
            logger.error("Exception when calling method patch_namespaced_deployment_config: %s\n", e)

    def list_pods_in_a_namespace(self, namespace, label_selector=''):
        """
        Method to list details for all or a specific type of pod within
        a namespace. If no parameter is given, it defaults to listing
        details for all pod types.
        :param namespace: The namespace containing the targeted pod
        :param label_selector: used to filter the types of pods
                               to be retrieved
        :return: A V1PodList object on success. None on failure
        """
        api_instance = k8sclient.CoreV1Api()
        api_response = None
        try:
            api_response = api_instance.list_namespaced_pod(namespace, label_selector=label_selector)
        except ApiException as e:
            logger.error("Exception when calling method list_namespaced_pod: %s\n", e)
        return api_response

    def list_pods_in_a_deployment(self, namespace, dc):
        """
        Method that returns a list of Pods belonging to
        a Deployment Config in a specific namespace
        :param namespace: The namespace where the dc is deployed
        :param dc: The Deployment Config for which we want to
                   retrieve the Pods
        :return: The name of the initial pod created as part of a deployment config.
                None on failure.
        """
        pods_in_dc = None
        pods_in_namespace = self.list_pods_in_a_namespace(namespace, label_selector='deploymentconfig')
        if pods_in_namespace is not None:
            pod_list = pods_in_namespace.items
            pods_in_dc = [pod.metadata.name for pod in pod_list if
                          pod.metadata.annotations['openshift.io/deployment-config.name'] == dc]
        return pods_in_dc

    def list_pods_in_all_namespaces(self, label_selector=''):
        """
        Method to list details for all or a specific type of pod within
        all namespaces. If no parameter is given, it defaults to listing
        details for all pod types.
        :param label_selector: used to filter the types of pods
                               to be retrieved
        :return: A V1PodList object on success. None on failure
        """
        api_instance = k8sclient.CoreV1Api()
        api_response = None
        try:
            api_response = api_instance.list_pod_for_all_namespaces(label_selector=label_selector)
        except ApiException as e:
            logger.error("Exception when calling method list_pod_for_all_namespaces: %s\n", e)
        return api_response

    def list_pod_state(self, namespace, pod_name):
        """
        Method for inspecting the state of a specific pod
        within a namespace
        :param namespace: The namespace containing the targeted pod
        :param pod_name: The targeted pod to be listed.
        :return: A V1Pod object on success. None on failure
        """
        api_instance = k8sclient.CoreV1Api()
        api_response = None
        try:
            api_response = api_instance.read_namespaced_pod_status(pod_name,
                                                                   namespace,
                                                                   pretty=self.pretty)
        except ApiException as e:
            logger.error("Exception when calling method read_namespaced_pod_status: %s\n", e)
        if api_response is not None:
            return api_response.status.container_statuses
        else:
            return api_response

    def list_deployment_in_a_namespace(self, namespace, dc):
        """
        Method to list details of a deployment config
        within a namespace
        :param namespace: The namespace containing the targeted
                          deployment config.
        :param dc: The targeted deployment config to be listed
        :return: A V1DeploymentConfig object on success. None on failure
        """
        api_instance = ocpclient.OapiApi()
        api_response = None
        try:
            api_response = api_instance.read_namespaced_deployment_config(dc, namespace)
        except ApiException as e:
            logger.error("Exception when calling method read_namespaced_deployment_config: %s\n", e)
        return api_response

    def list_all_deployments_in_a_namespace(self, namespace):
        """
        Method that lists all objects of type DeploymentConfig
        within a namespace
        :param namespace: The namespace where to search for dcs
        :return: A V1DeploymentConfigList object on success. None on failure
        """
        api_instance = ocpclient.OapiApi()
        api_response = None
        try:
            api_response = api_instance.list_namespaced_deployment_config(namespace, pretty=self.pretty)
        except ApiException as e:
            logger.error("Exception when calling method list_namespaced_deployment_config: %s\n", e)
        return api_response

    def list_deployments_in_all_namespaces(self, label_selector=''):
        """
        Method that lists all deployment configs across all
        namespaces in a cluster.
        :param label_selector: Used to filter the types of dcs
                               to be selected.
        :return: A V1DeploymentConfigList object on success. None on failure
        """
        api_instance = ocpclient.OapiApi()
        api_response = None
        try:
            api_response = api_instance.list_deployment_config_for_all_namespaces(label_selector=label_selector)
        except ApiException as e:
            logger.error("Exception when calling method list_deployment_config_for_all_namespaces: %s\n", e)
        return api_response

    def find_unhealthy_dcs_in_namespace_list(self, dc_list):
        """
        :param dc_list: A list of objects of type V1DeploymentConfig
        :return: A list of objects of type DeploymentConfig if any.
        """
        # Every dc object has a status key containing a conditions list.
        # The conditions list contains exactly two objects of type v1.DeploymentCondition,
        # the first object of the two being of type 'Available' and the second 'Progressing'
        # If neither has a False status, we treat the corresponding dc as unhealthy.
        unhealthy_dcs = []
        for dc in dc_list:
            if dc.status.conditions[0].status == 'False' and dc.status.conditions[1].status == 'False':
                unhealthy_dcs.append(dc)
        return unhealthy_dcs

    def poll_dc_readiness_in_a_namespace(self, namespace, dc):
        """
        :param namespace: The namespace containing the targeted
                          deployment config.
        :param dc: The deployment config we are polling status for.
        :return: boolean
        ;raise: ocp_exceptions.OcpDeploymentConfigTerminatedError in case
            if deployment config is terminated
        """
        # We first need to check that the conditions list in the status
        # object of the dc object contains two objects for dc progression
        # as well as dc availability
        self.check_dc_status_conditions_availability(namespace, dc)
        # Check and return the readiness of the dc as a boolean.
        # The dc is only ready when availability and
        # progression are both set to 'True'
        dc_ready = False
        dc_obj = self.list_deployment_in_a_namespace(namespace, dc)
        status_conditions_list = dc_obj.status.conditions
        availability = [s for s in status_conditions_list if s.type == 'Available'][0]
        progression = [s for s in status_conditions_list if s.type == 'Progressing'][0]
        if availability.status == 'True' and progression.status == 'True':
            logger.info("!!! Deployment %s in namespace %s  is in ready state !!!", dc, namespace)
            dc_ready = True
        elif availability.status == 'False' and progression.status == 'False':
            dc_log = self.read_dc_log(namespace, dc)
            logger.error("The dc: %s is in a terminated state. See the log entries below:", dc)
            for line in dc_log:
                logger.error(line)
            raise ocp_exceptions.OcpDeploymentConfigTerminatedError(
                "The dc: %s in namespace %s is in a terminated state." %
                (dc, namespace))
        elif progression.status == 'Unknown' or (progression.status == 'False' and availability.status == 'False'):
            logger.info("Waiting for dc %s to become available ...", dc)
        return dc_ready

    def check_dc_status_conditions_availability(self, namespace, dc):
        """
        Helper function that checks the needed parameters in the
        status object belonging to a deployment config (dc) are
        available before we make any subsequent calls that depend
        on the availability of those parameters. Specifically, we
        are looking for two objects under the conditions list,
        progression and availability
        :param namespace: The namespace containing the targeted
                          deployment config
        :param dc: The targeted deployment config
        :return: None
        """
        # TODO: Figure out if this method should return something
        dc_status_conditions_unavailable = True
        while dc_status_conditions_unavailable:
            d_c = self.list_deployment_in_a_namespace(namespace, dc)
            if d_c is None:
                # TODO: Return appropriate value when there is no dc in namespace
                pass
            else:
                sc = d_c.status.conditions
                if sc is not None and len(sc) == 2:
                    dc_status_conditions_unavailable = False
                else:
                    logger.info("Waiting for status info to become available for dc: %s", dc)
                    sleep(5)
                    pass

    def read_dc_log(self, namespace, dc, tail_lines=5):
        """
        Method to read the logs of a deployment config
        within a namespace. Returns a list of lines of
        requested log file.
        :param namespace: The namespace where the targeted dc resides
        :param dc: The targeted deployment config
        :param tail_lines: The number of most recent lines in the log
                           to be displayed.
        :return: A list of strings.
        """
        api_instance = ocpclient.OapiApi()
        api_response = None
        try:
            api_response = api_instance.read_namespaced_deployment_config_log(dc,
                                                                              namespace,
                                                                              tail_lines=tail_lines,
                                                                              _preload_content=False)
            api_response = api_response.read().splitlines()
        except ApiException as e:
            logger.error("Exception when calling method read_namespaced_deployment_config_log: %s\n", e)
        return api_response

    def list_dc_events_in_a_namespace(self, namespace, dc):
        """
        Method that lists the events of Pods belonging to a specific
        Deployment Config in a specific namespace
        :param namespace: The namespace where the targeted dc resides
        :param dc: The Deployment Config whose pods we want to retrieve
                   events for.
        :return: A list of objects of type V1Event on success. None on failure.
        """
        pods_in_dc = self.list_pods_in_a_deployment(namespace, dc)
        api_instance = k8sclient.CoreV1Api()
        api_response = None
        dc_pod_events = None
        try:
            api_response = api_instance.list_namespaced_event(namespace, pretty=self.pretty).items
        except ApiException as e:
            logger.error("Exception when calling method list_deployment_config_for_all_namespaces: %s\n", e)

        if api_response is not None:
            try:
                dc_pod_events = [de for de in api_response if (de.involved_object.kind == 'Pod' and
                                                               de.involved_object.name in pods_in_dc)]
            except KeyError as e:
                logger.error("The key you are searching for is not available")
        return dc_pod_events
