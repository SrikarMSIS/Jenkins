#Take Inputs from the Jenkins Job
#Write a TCL File using the Job Inputs
#Enter the Cadence Shell
import logging
import sys
import os
import shutil
from datetime import datetime
import json

# Configure logging
logging.basicConfig(

    level=logging.INFO,  # Set the logging level to INFO

    format='%(asctime)s - %(levelname)s - %(message)s',  # Set the format for log messages

    stream=sys.stdout  # Output logs to standard output

)

class Synthesis:
    #Constructor
    def __init__(self, tech, rtlFile, effortSet, constraints, format):
        self.logPath = "/home/vlsi/srikar/jenkins_auto"
        self.rtlFile = rtlFile
        self.constraints = constraints
        self.technology = tech
        self.effort = effortSet
        self.format = format
        self.newPath = None
        self.reqJson = "/home/vlsi/srikar/jenkins_auto/required.json"
        self.libraryPath = None
        self.svTemp = "/home/vlsi/srikar/jenkins_auto/synthesis_sv_temp.tcl"
        self.vTemp = "/home/vlsi/srikar/jenkins_auto/synthesis_v_temp.tcl"
        self.tclPath = None
    
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
        to the new self.newPath location

        Inputs: Self
        Outputs: None

        """
        try:
            logging.info("----Changing the working path")
            current_time = datetime.now()
            formatted_time = current_time.strftime('%Y-%m-%d_%H-%M-%S')
            filename_with_extension = self.rtlFile.split('/')[-1]
            filename_without_extension = filename_with_extension.split('.')[0]
            folder_name = "output_files_" + filename_without_extension + "_" + formatted_time
            folder_path = os.path.join(self.logPath,folder_name)
            os.makedirs(folder_path)
            os.chdir(folder_path)
            logging.info(f"----The output path is : {folder_path}")
            self.newPath = folder_path
            shutil.copy(self.rtlFile, self.newPath)

        except Exception as exception:
            logging.error(f"Exception: {exception}")
            logging.error(f"Exiting Execution")

        return 0
    
    @staticmethod
    def createTcl(content, path):
        """
        This function takes the TCL Content and then write it to the new path
        Inputs: TCL Content, self.new_path
        Returns: New TCL Script Path

        """
        try:
            tclFileName = "synthesis.tcl"
            tclPath = os.path.join(path, tclFileName)
            with open(tclPath, 'w') as file:
                file.write(content)
            logging.info(f"TCL Script Written in the path: {tclPath}")
        
        except Exception as exception:
            logging.info(f"---Exception: {exception}")
            logging.info("---Stopping Execution")
            sys.exit()
        
        return tclPath
            
        
    def writeTcl(self):
        """
        This function takes the job inputs - Tech and RTL Format and writes a new file based on the inputs
        This new synthesis tcl file is written to the working path

        Inputs: Self
        Returns: None

        """

        try: 
            if(os.path.isfile(self.newPath)):
                with open(self.reqJson, 'r') as json_file:
                    json_data = json.load(json_file)

                self.libraryPath = json_data[self.technology]["Synthesis"]["lib"]
                if(self.format == 'v'):
                    with open(self.vTemp, 'r') as file:
                        tcl_content = file.read()
                    filename_with_extension = self.rtlFile.split('/')[-1]
                    modified_content = tcl_content.replace('{library_path}', self.libraryPath).replace('{rtl_file}', filename_with_extension).replace('{effort}', self.effort)
                else:
                    with open(self.svTemp, 'r') as file:
                        tcl_content = file.read()
                    filename_with_extension = self.rtlFile.split('/')[-1]
                    modified_content = tcl_content.replace('{library_path}', self.libraryPath).replace('{rtl_file}', filename_with_extension).replace('{effort}', self.effort)
                self.tclPath = self.createTcl(modified_content, self.newPath)

            else:
                logging.error(f"----RTL Not Copied to {self.newPath}")
                logging.error("----Exiting Execution")
                sys.exit()
        except Exception as exception:
            logging.error(f"----Exception: {exception}")
            logging.error(f"-----Exiting Execution")
            sys.exit()
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

            #Admin Job - For Logging
            syn.adminJob()

            #Change Directory
            syn.chngDir()

            #Write TCL Script from Template
            syn.writeTcl()
        else:
            logging.info("No Parameter Passed")
    except Exception as exception:
        logging.error(f"Exception: {exception}")
        logging.error(f"Exiting Execution")
        sys.exit()
    return 0

if __name__ == '__main__':
    main()
