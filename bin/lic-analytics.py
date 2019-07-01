##################################
#Name: lic-analytics.py
#Purpose: Do analytics of lic data
#Author:
#Version:
###################################
import configparser
import time
from datetime import datetime
import pyAesCrypt
import sys
import logging.config
import os
import pandas

logging.basicConfig(filename='lic-analytics-service.log',filemode='a',format='%(asctime)s | %(levelname)s | %(message)s',datefmt='%H:%M:%S',level=logging.DEBUG)
logger = logging.getLogger(__name__)

def agent_reports(config):
    print("Entered in agent_report() function")
    #Parse/Read CSV file using panda math library and in future we will read it from mysql database
    result = pandas.read_csv('..\data\lic-data-dev.csv')
    print(result)

def check_conditions_to_start(argv):
    logger.info("Entered in check_conditions_to_start() function...")
    if len(argv) < 3:
        logger.error("Please provide Decryption Password as first argument and Environment as second!")
        logger.error("Supported Env are: DEV, PRD")
        sys.exit(1)
    else:
        env = sys.argv[2]
        if env in "DEV PRD":
            logger.info("Checking LIC Analytics for Environment:[{0}]".format(env))
        else:
            logger.error("[{}] is not supported Environment for LIC Analytics!Exiting!".format(env))
            sys.exit(1)

def config_test(config,env):
    logger.debug("Entered in config_test() function...")
    # Read values from .ini based file
    try:
       data_file = config[env]['data_file']
       logger.debug("Using data file name:{0}".format(data_file))
    except:
        logger.exception("Configuration is not correct. Please make sure you have all required key value pair set")
        sys.exit(1)

# Main function
if __name__ == "__main__":
    logger.debug("*************************************************")
    logger.debug("** Starting LIC Analytics Service built by Virender **")
    logger.debug("*************************************************")
    start_time = time.time()
    check_conditions_to_start(sys.argv)

    password = sys.argv[1]
    env = sys.argv[2]
    # Decrypt configs file before Use
    bufferSize = 64 * 1024

    if os.name == 'nt':
        print("Running on Windows Platform:[{0}]".format(os.name))
        output_config_file = "..\configs\lic-analytics-configs.ini"
        input_encrypted_config_file = "..\configs\lic-analytics-configs.aes"
        #print("In:{0}  , Out:{1}".format(input_encrypted_config_file,output_config_file))
    else:
        print("Running on Linux Platform:[{0}]".format(os.name))
        output_config_file = "../configs/lic-analytics-configs.ini"
        input_encrypted_config_file = "../configs/lic-analytics-configs.aes"

    try:
        #print("---- > 0:{0},1:{1},2:{2}".format(input_encrypted_config_file,output_config_file,password))
        pyAesCrypt.decryptFile(input_encrypted_config_file,output_config_file,password, bufferSize)
    except:
        logger.error("Decryption password is not correct.Exiting!")
        print("Password:{0} ".format(password))
        sys.exit(1)

    # Read values from .ini based file
    config = configparser.ConfigParser()
    config.read(output_config_file)
    config_test(config, env)

    agent_reports(config)
    logger.debug("** Program Completed! **")
    print("**Program Completed.Please check log files**")