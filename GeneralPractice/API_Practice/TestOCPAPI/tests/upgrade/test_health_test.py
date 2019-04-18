import pytest
from ocp_health_check import OcpHealthCheck
from glusto.core import Glusto as g


""" OCP Health Check test """

'''
Created on Apr 2, 2019

@author: Redhat CSS-QI

'''


@pytest.mark.check_nodes_health_test
def test_check_nodes_health():
    """Verify that Check that all the nodes in the cluster are healthy:

    """
    namespace = g.config['ocp_logging_project_name']
    obj_ocp_health = OcpHealthCheck()
    assert obj_ocp_health.check_nodes_health() is True


