#Take Inputs from the Jenkins Job
#Write a TCL File using the Job Inputs
#Enter the Cadence Shell
import logging as log
import sys
import os
import glob

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
            log.info("----WELCOME TO JENKINS AUTOMATION----")
            log.info("----RUNNING SYNTEHSIS----")
            log.info(f"Working Path: {self.workingPath}")
            log.info(f"Technology : {self.technology}")
        except Exception as exception:
            log.error(f"Exception: {exception}")
            log.error(f"Exiting Execution")
            sys.exit()
        return 0

def main():
    try:
        workingPath = input("Input to the working Path")
        rtlFile = input("Please enter the RTL Explicit Path")
        tech = input("Enter the Technology you want to associate your work with")
        constraints = input("Please enter the constraints")
        #Create instance
        syn = Synthesis(workingPath, rtlFile, constraints, tech)
        syn.adminJob()
    except Exception as exception:
        log.error(f"Exception: {exception}")
        log.error(f"Exiting Execution")
        sys.exit()
    return 0

if __name__ == '__main__':
    main()