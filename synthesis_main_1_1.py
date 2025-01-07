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
    def __init__(self, tech, rtlFile, effortSet, constraints, format):
        self.logPath = None
        self.rtlFile = rtlFile
        self.constraints = constraints
        self.technology = tech
        self.effort = effortSet
        self.format = format
    
    def adminJob(self):
        """
        This function is used to initially run the logging info of the job

        Inputs: Self
        Returns: None

        """
        try:
            logging.info("----WELCOME TO JENKINS AUTOMATION")
            logging.info("----RUNNING SYNTEHSIS")
            logging.info(f"Technology : {self.technology}")
            logging.info(f"RTL File : {self.rtlFile}")
        except Exception as exception:
            logging.error(f"Exception: {exception}")
            logging.error(f"Exiting Execution")
            sys.exit()
        return 0

    def chngDir(self):
        """
        Change the Directory and Copy the RTL File from the previous location
        to the new self.logPath location

        Inputs: Self
        Outputs: None

        """
        try:
            logging.info("----Changing the working path")
        except Exception as exception:
            logging.error(f"Exception: {exception}")
            logging.error(f"Exiting Execution")
        return 0


def main():
    try:
        if len(sys.argv) > 1:
            tech = sys.argv[1]
            rtlFile = sys.argv[2]
            effortSet = sys.argv[3]
            constraints = sys.argv[4]
            format = sys.argv[5]
            #Create instance
            syn = Synthesis(tech, rtlFile, effortSet, constraints, format)
            syn.adminJob()
            syn.chngDir()
        else:
            logging.info("No Parameter Passed")
    except Exception as exception:
        logging.error(f"Exception: {exception}")
        logging.error(f"Exiting Execution")
        sys.exit()
    return 0

if __name__ == '__main__':
    main()