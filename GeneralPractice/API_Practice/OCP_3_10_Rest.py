'''
Created on Nov 2, 2018
/home/gkimetto/Og_Selenium/Cockpit3_5/REST_Practice/src/OCP_3_10_Rest.py

@author: gkimetto
'''
import __main__

"""Import necessary libraries"""
import time
import pyyaml
import logging
import requests
import os
#from  ocp_logging_configs.yml.py import common
import argparse



parser = argparse.ArgumentParser(description='Select a type of OCP Logging \
         test to run')

parser.add_argument("--test_type",help="OpenShift Logging Test type options \
         include: baseline, negative.\n", default="baseline", \
         choices =["baseline", "negative","scaling"])

# Check if OpenShift Logging Directory exists if not create it 
ocp_logging_dir= "./ocp_logs"


if not os.path.exists(ocp_logging_dir):
    os.mkdir(ocp_logging_dir)

# Start basic logging for troubleshooting

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s ',
                    filename='./ocp_logs/ocp_logging_test.log', filemode='w',
                    level=logging.INFO)

# Get the configuration details from the config file to a large dictionary 
__all__ = ['CONF']
 
CONF = list(yaml.load_all(open("./ocp_logging_configs.yml")))[0]

try:
        public_ip = CONF.get('common').get('lbs').get('lb1')
except: 
        logging.info("Unable to locate Load Balancer. Checking for any Master(s)")
        try:
            public_ip = CONF.get('common').get('masters').get('master1')
        except:
            logging.info("Unable to locate a Master. Invalid Configuration File")



# Populate the inventory file as per configuration file
# SKIP --Created inventory manually

#Get the OCP public URL either by Loadbalancer IP or 1st master (single master) 
# If a load balancer is in use setup the public RUL with the LB
def get_public_ocp_url(public_ip):
    

    ocp__public_url= "https://"+public_ip+ ":8443" 
    logging.info("Public OCP URL : "+ocp__public_url)
    print ("Public URL : " + ocp__public_url)
    print ("-"*50)
    return ocp__public_url


# 
# 
# 
# 
# """Create a token Login to OCP and get session token"""
# """ Create a service account 'ocp_logging' and grant a role to to it.
# """
# oc create serviceaccount ocp-logging-usr
# 
# 
# """Authenticate via secure token avoid clear text or use the client
# authenticate API calls with an access token or X.509 certificate."""
#  
# oc policy add-role-to-user admin system:serviceaccounts:test:ocp-logging-usr
# 
# ocp_logging_token = oc serviceaccounts get-token ocp-logging-usr
# 
# 
# curl -X GET -H "Authorization: Bearer ocp_logging_token" https://selt-vm1.css.lab.eng.rdu2.redhat.com:8443/oapi/v1 --insecure


def check_requirements():
    """
        Purpose:
        CSS-XXX
        Check that the requiremensts are met
    """
    logging.info("Checking System Requirements are met -if not met install them.")


def main():
    
    # Check the option selected and call the appropriate method
    args = parser.parse_args()
    
    test_type = args.test_type
    print ("Starting "+ test_type+ " Tests ")
    logging.info ("-"*50)
    logging.info("Starting "+ test_type+ " Tests ")
    get_public_ocp_url(public_ip)

if __name__=="__main__":
    main()