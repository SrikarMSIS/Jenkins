#Take Inputs from the Jenkins Job
#Write a TCL File using the Job Inputs
#Enter the Cadence Shell
import logging
import sys
import os
import glob

# Configure logging

logging.basicConfig(

    level=logging.INFO,  # Set the logging level to INFO

    format='%(asctime)s - %(levelname)s - %(message)s',  # Set the format for log messages

    stream=sys.stdout  # Output logs to standard output

)

class Synthesis:
    #Constructor
    def __init__(self, workingPath, rtlFile, constraints, tech):
        self.workingPath = workingPath
        self.logPath = None
        self.rtlFile = rtlFile
        self.constraints = constraints
        self.technology = tech
    
    def adminJob(self):
        try:
            logging.info("----WELCOME TO JENKINS AUTOMATION----")
            logging.info("----RUNNING SYNTEHSIS----")
            logging.info(f"Working Path: {self.workingPath}")
            logging.info(f"Technology : {self.technology}")
            logging.info(f"RTL File : {self.rtlFile}")
        except Exception as exception:
            logging.error(f"Exception: {exception}")
            logging.error(f"Exiting Execution")
            sys.exit()
        return 0

def main():
    try:
        if len(sys.argv) > 1:
            workingPath = sys.argv[1] 
            rtlFile = sys.argv[2]
            tech = sys.argv[3]
            constraints = sys.argv[1]
            #Create instance
            syn = Synthesis(workingPath, rtlFile, constraints, tech)
            syn.adminJob()
        else:
            logging.info("No Parameter Passed")
    except Exception as exception:
        logging.error(f"Exception: {exception}")
        logging.error(f"Exiting Execution")
        sys.exit()
    return 0

if __name__ == '__main__':
    main()