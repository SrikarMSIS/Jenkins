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
    #Constructor
    def __init__(self, tech, synFiles):
        self.logPath = "/home/vlsi/srikar/jenkins_auto"
        self.synFiles = synFiles
        self.technology = tech
        self.flp_path = None
        self.reqJson = "/home/vlsi/srikar/jenkins_auto/required.json"

    
    def adminJob(self):
        """
        This function is used to execute the admin printing jobs

        Inputs: Self
        Returns: None
        
        """
        try:
            logging.info("----WELCOME TO JENKINS AUTOMATION")
            logging.info("----RUNNING SYNTEHSIS")
            logging.info(f"Technology : {self.technology}")
            logging.info(f"Synthesis File : {self.synFiles}")
        except Exception as exception:
            logging.error(f"-Exception: {exception}")
            logging.error(f"-Exiting Execution")
            sys.exit()

        return 0
    
    def chngDir(self):
        """
        This shall change to the directory created from the synthesis file
        Post this, creating a directory called Floorplan
        Further processes, shall be done in the created folder
        
        Inputs: Self
        Returns: None

        """
        try:
            logging.info("----Changing the Working Path")
            logging.info(f"Changing to: {self.synFiles}")
            os.chdir(self.synFiles)
            flp_folder_name = "floorplan"
            flp_folder_path = os.path.join(self.synFiles,flp_folder_name)
            os.makedirs(flp_folder_path)
            if(os.path.exists(flp_folder_path)):
                logging.info("---Floorplan Folder created")
                os.chdir(flp_folder_path)
                self.flp_path = flp_folder_path
                logging.info(f"--Working in {self.flp_path}")
            else:
                logging.error("--Floorplan Folder Not Created")
                sys.exit()

        except Exception as exception:
            logging.error(f"--Exception Incurred: {exception}")
            logging.error("Exiting Simulation")
            sys.exit()
        return 0
    
    def writeTcl(self):
        """
        This function is used to write to a TCL file based on the input
        The standard inputs are read from a JSON File.
        The path of this is same as the self.flp_path

        Inputs: Self
        Outputs: None
        
        """
        try:
            if(os.path.exists(self.flp_path)):
                with open(self.reqJson, 'r') as jsonFile:
                    jsonData = json.load(jsonFile)
                
        except Exception as exception:
            logging.error(f"---Exception Occured: {exception}")
            logging.error("Exiting Simulation")       
            sys.exit()
        return 0



def main():
    try:
        if len(sys.argv) > 1:
            tech = sys.argv[1]
            synFiles = sys.argv[2]
    
            #Create instance
            flp = Floorplan(tech, synFiles)

            # #Admin Job - For Logging
            flp.adminJob()

            #Change Directory
            flp.chngDir()

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
