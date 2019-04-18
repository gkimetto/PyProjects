"""
Setting pytest config files to be used by test fixtures defined under ocp_cns_upgrade
"""
import os
import pytest
from glusto.core import Glusto as g


def pytest_addoption(parser):
    parser.addoption("--openshift-version", action="store", default='latest',
                     help="Version of OpenShift to test against for functional tests")
    parser.addoption("--openshift-first-master", action="store",
                     help="Openshift first master HOSTNAME/IP")
    parser.addoption("--openshift-default-tests-config", action="store",
                     help="Openshift default tests config file")
    parser.addoption("--openshift-tests-log-dir", action="store", default="./logs/",
                     help="Openshift tests logs dir")
    parser.addoption("--openshift-tests-log-level", action="store", default="INFO",
                     help="Openshift tests log level")
    parser.addoption('--log-to-stdout', action='store', default="True",
                     help="Log output to stdout as well as file")


def pytest_report_header(config):
    return "OpenShift version: {}".format(config.getoption('--openshift-version'))


@pytest.fixture(scope="session")
def load_config_file():
    """ Fixture to load config files and returns a dict"""
    def _load_config_file(config_filename, config_file_type=None):
        # Get file type
        if config_file_type is None:
            _, config_file_type = os.path.splitext(config_filename)
            config_file_type = config_file_type.replace('.', '')

        # load config file
        config = g.load_config(config_filename, config_type=config_file_type)
        return config
    return _load_config_file


@pytest.fixture(scope="session", autouse=True)
def get_openshift_cluster_info(request, load_config_file):
    """ Fixture to get openshift cluster info """
    openshift_tests_log_dir = request.config.getoption('--openshift-tests-log-dir')
    openshift_tests_log_level = request.config.getoption('--openshift-tests-log-level')
    log_to_stdout = request.config.getoption('--log-to-stdout')
    log_name = "ocp_tests_log"

    # Create log dir if logs dir does not exist.
    openshift_tests_log_dir = os.path.abspath(openshift_tests_log_dir)
    if not os.path.exists(openshift_tests_log_dir):
        os.makedirs(os.path.abspath(openshift_tests_log_dir))

    # Define filename with timestamp
    filename = os.path.join(openshift_tests_log_dir,
                            ('ocp_tests_log_%s.log' %
                             datetime.now().strftime("%Y_%m_%d_%H_%M_%S")))

    g.log = g.create_log(name=log_name, filename=filename,
                         level=openshift_tests_log_level)

    if 'true' in log_to_stdout.lower():
        g.add_log(g.log, filename='STDOUT')

    default_ocp_tests_config_file = request.config.getoption('--openshift-default-tests-config')
    if default_ocp_tests_config_file is not None:
        config = load_config_file(default_ocp_tests_config_file)
        g.update_config(config)

    openshift_cluster_config = {}
    openshift_first_master = request.config.getoption('--openshift-first-master')
    openshift_cluster_config['first_master'] = openshift_first_master
    # TODO'S Get master, nodes, OcpAppMgmt instance here.

    g.update_config(openshift_cluster_config)
    g.log.info("openshift tests default configs:\n%s", g.config)
