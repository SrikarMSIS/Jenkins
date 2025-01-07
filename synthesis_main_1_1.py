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
            print("----WELCOME TO JENKINS AUTOMATION----")
            print("----RUNNING SYNTEHSIS----")
            print(f"Working Path: {self.workingPath}")
            print(f"Technology : {self.technology}")
            print(f"RTL File : {self.rtlFile}")
        except Exception as exception:
            log.error(f"Exception: {exception}")
            log.error(f"Exiting Execution")
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
            print("No Parameter Passed")
    except Exception as exception:
        log.error(f"Exception: {exception}")
        log.error(f"Exiting Execution")
        sys.exit()
    return 0

if __name__ == '__main__':
    main()