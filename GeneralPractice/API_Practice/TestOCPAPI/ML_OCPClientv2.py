#!/usr/bin/python
import warnings
from urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)
from kubernetes import client, config
from openshift.dynamic import DynamicClient
from kubernetes.client.rest import ApiException
from pprint import pformat
import json
from subprocess import PIPE, Popen
import requests
from time import sleep
import logging
import ocp_exceptions
from pprint import pprint


# Initiate child logger. Parent logger is in the script invoking this
# module and is named 'ocp_test_logger'
logger = logging.getLogger('ocp_test_logger.ocp_mgmt')

class OcpMgmt(object):

    def __init__(self, token, hostname='localhost'):
        
        configuration = client.Configuration()
        configuration.api_key['authorization'] = token
        configuration.api_key_prefix['authorization'] = 'Bearer'
        configuration.host = 'https://%s:8443' % hostname
        configuration.verify_ssl = False

        k8s_client = client.ApiClient(configuration)
        self.dyn_client = DynamicClient(k8s_client)

    @classmethod
    def get_auth_token(self, hostname='localhost'):
        """
        Method that returns a session token to be used for REST calls
        using the requests modules
        :return: Authentication token
        """
        try:
            p1 = Popen(["curl", "-sIk",
                        """https://%s:8443/oauth/authorize?response_type=token"""
                        """&client_id=openshift-challenging-client""" % hostname,
                        "--user", "admin:redhat"], stdout=PIPE) 
            p2 = Popen(["grep", "-oP", "access_token=\\K[^&]*"], stdin=p1.stdout, stdout=PIPE)
            p1.stdout.close()
        except ApiException as e:
            logger.error("Exception was encountered while trying to obtain a session token: %s\n", e)
        token = p2.communicate()[0]
        return token.strip().decode('ascii')

    def list_project(self, namespace=None):

        v1_projects = self.dyn_client.resources.get(api_version='project.openshift.io/v1', kind='Project')

        project_list = v1_projects.get()

        for project in project_list.items:
            print(project.metadata.name)