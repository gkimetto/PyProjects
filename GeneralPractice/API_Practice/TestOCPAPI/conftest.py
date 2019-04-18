"""
Setting pytest config files to be used by test fixtures defined under ocp_cns_upgrade
"""
import os
import pytest
from ocp_exceptions import (ExecutionError, ConfigError)
from glusto.core import Glusto as g


@pytest.fixture(scope="session", autouse=True)
def setup_ocp_health_checker():
    """ Read configs, Initialize variables and setup ocp for running health checks"""
    g.log.info("Setting up necessary parameters for cluster health checker.")

    # Get first master in the cluster
    if 'first_master' in g.config and g.config['first_master']:
        first_master = g.config.get('first_master')
    else:
        raise ConfigError("Key Error: Unable to get 'first_master' "
                          "from g.config:\n %s" % g.config)

    # Get ocp_user
    if g.config.get("ocp_user"):
        ocp_user = g.config.get("ocp_user")
    else:
        ocp_user = "admin"

    # Get ocp_pass
    if g.config.get("ocp_pass"):
        ocp_pass = g.config.get("ocp_pass")
    else:
        ocp_pass = "redhat"

    # Get ocp inventory file path on master
    if g.config.get("ocp_inventory_file"):
        ocp_inventory_file = g.config.get("ocp_inventory_file")
    else:
        ocp_inventory_file = "/root/ocp_install_hosts"