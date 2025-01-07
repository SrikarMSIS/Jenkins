#Take Inputs from the Jenkins Job
#Write a TCL File using the Job Inputs
#Enter the Cadence Shell
import logging
import sys
import os
import glob


# ANSI escape codes for colors

GREEN = "\033[92m"  # Green text

YELLOW = "\033[93m"  # Yellow text

RED = "\033[91m"     # Red text

RESET = "\033[0m"    # Reset to default color


# Custom logging formatter to add color

class ColoredFormatter(logging.Formatter):

    def format(self, record):

        if record.levelno == logging.INFO:

            record.msg = f"{GREEN}{record.msg}{RESET}"

        elif record.levelno == logging.WARNING:

            record.msg = f"{YELLOW}{record.msg}{RESET}"

        elif record.levelno == logging.ERROR:

            record.msg = f"{RED}{record.msg}{RESET}"

        return super().format(record)


# Configure logging

formatter = ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s')

handler = logging.StreamHandler(sys.stdout)

handler.setFormatter(formatter)


logging.basicConfig(

    level=logging.INFO,  # Set the logging level to INFO

    handlers=[handler]   # Use the custom handler

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