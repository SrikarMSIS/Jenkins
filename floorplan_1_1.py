#Take Inputs from the Jenkins Job
#Write a TCL File using the Job Inputs
#Enter the Cadence Shell
import logging
import sys
import os
import shutil
from datetime import datetime
import json
import subprocess

# Configure logging
logging.basicConfig(

    level=logging.INFO,  # Set the logging level to INFO

    format='%(asctime)s - %(levelname)s - %(message)s',  # Set the format for log messages

    stream=sys.stdout  # Output logs to standard output

)

class Floorplan:
    def __init__(self, tech, synFiles):
        self.tech = tech
        self.synFiles = synFiles
    
    def adminJob(self):
        """
        This function is used to initially run the logging info of the job

        Inputs: Self
        Returns: None

        """
        try:
            logging.info("----WELCOME TO JENKINS AUTOMATION")
            logging.info("----RUNNING FLOORPLAN")
            logging.info(f"Technology : {self.technology}")
            logging.info(f"Working Files Path : {self.synFiles}")
        except Exception as exception:
            logging.error(f"-Exception: {exception}")
            logging.error(f"-Exiting Execution")
            sys.exit()
        return 0
        
    def create_change_pwd(self):
        """
        This function is to copy the netlist.v files with the sdc files to 
        a new folder in the main directory called floorplan
        And then, the path is updates
        Inputs: Self
        Returns: None

        """

        
        return 0

def main():
    try:
        if len(sys.argv) > 1:
            tech = sys.argv[1]
            synFiles = sys.argv[2]
            effortSet = sys.argv[3]
            constraints = sys.argv[4]
            format = sys.argv[5]
            #Create instance
            flp = Floorplan(tech, synFiles)

            #Admin Job - For Logging
            flp.adminJob()

            #Create Directory and change Working Path
            flp.create_change_pwd()

            # #Change Directory
            # syn.chngDir()

            # #Write TCL Script from Template
            # syn.writeTcl()

            # #Change Directory to New Directory
            # syn.tclDir()

            # #Enter the Cadence shell and perform genus operation
            # syn.genusFlow()
        else:
            logging.info("No Parameter Passed")
    except Exception as exception:
        logging.error(f"-----Exception: {exception}")
        logging.error(f"------Exiting Execution")
        sys.exit()
    return 0

if __name__ == '__main__':
    main()
