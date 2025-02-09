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

class Xcelium:
    #Constructor
    def __init__(self, topmodule, bottomModule):
        self.topmodule = topmodule
        self.bottomModule = bottomModule
        self.logPath = "/home/vlsi/srikar/jenkins_auto"
        self.filename_with_extension_top = self.topmodule.split('/')[-1]
        self.filename_with_extension_bottom = self.bottomModule.split('/')[-1]
        # self.constraints = constraints
        # self.technology = tech
        # self.effort = effortSet
        # # self.format = format
        self.newPath = None
        self.xceliumPath = None
        # self.reqJson = "/home/vlsi/srikar/jenkins_auto/required.json"
        # self.libraryPath = None
        # self.svTemp = "/home/vlsi/srikar/jenkins_auto/synthesis_sv_temp.tcl"
        # self.vTemp = "/home/vlsi/srikar/jenkins_auto/synthesis_v_temp.tcl"
        # self.tclPath = None
    
    def adminJob(self):
        """
        This function is used to initially run the logging info of the job

        Inputs: Self
        Returns: None

        """
        try:
            logging.info("----WELCOME TO JENKINS AUTOMATION")
            logging.info("----RUNNING XCELIUM SIMULATION")
            logging.info(f"topmodule : {self.topmodule}")
            logging.info(f"BottomModule : {self.bottomModule}")
        except Exception as exception:
            logging.error(f"-Exception: {exception}")
            logging.error(f"-Exiting Execution")
            sys.exit()
        return 0

    def chngDir(self):
        """
        Change the Directory and Copy the RTL File from the previous location
        to the new self.newPath location

        Inputs: Self
        Returns: None

        """
        try:
            logging.info("----Changing the working path")
            current_time = datetime.now()
            formatted_time = current_time.strftime('%Y-%m-%d_%H-%M-%S')
            
            filename_without_extension = self.filename_with_extension_top.split('.')[0]
            folder_name = "output_files_" + filename_without_extension + "_" + formatted_time
            folder_path = os.path.join(self.logPath,folder_name)
            os.makedirs(folder_path)
            os.chdir(folder_path)
            logging.info(f"----The output path is : {folder_path}")
            self.newPath = folder_path
            if(os.path.exists(self.newPath)):
                xcelium_folder_name = "simulation"
                xcelium_folder = os.path.join(self.newPath, xcelium_folder_name)
                os.makedirs(xcelium_folder)
                shutil.copy(self.filename_with_extension_top, self.filename_with_extension_bottom, xcelium_folder)
                self.xceliumPath = xcelium_folder
            else:
                logging.warning(f"Folder not created in: {self.newPath}")

        except Exception as exception:
            logging.error(f"--Exception: {exception}")
            logging.error(f"--Exiting Execution")

        return 0
    
    def xceliumFlow(self):
        """
        This function is used to enter the cadence shell and run the simulation using xcelium

        Inputs: Self
        Returns: None

        """
        try:#Write TCL Script from Template
            # syn.writeTcl()

            # #Change Directory to New Directory
            # syn.tclDir()

            logging.info("---------------")
            logging.info("--Entering the Cadence Shell")
            logging.info("---------------")
            source_cmd = f'sudo -u vlsi csh -c "source /home/install/cshrc && xrun -access +rwc {self.filename_with_extension_top} {self.filename_with_extension_bottom}"'
            subProcess = subprocess.Popen(source_cmd ,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
            stdout, stderr = subProcess.communicate()
            logging.info(f"Synthesis Output: {stdout}")
            logging.error(f"Synthesis Error: {stderr}")
            logging.info("--Synthesis Done")

        except Exception as exception:
            logging.error(f"!Execption: {exception}")
            logging.error(f"Stopping Simulation")
            sys.exit()

        return 0
    
    def generate_json_data(self):
        data = {
            "build_number" : os.environ.get("BUILD_NUMBER", "unknown"),
            "path" : self.newPath,
            "synthesis_path" : self.xceliumPath
        }

        return data
    
    @staticmethod
    def save_json_data(data, filename = "xcelium_build_info.json"):
        try:
            with open(filename, "w") as file:
                json.dump(data, file, indent = 4)
        
        except Exception as exception:
            logging.error(f"Exception: {exception}")
            logging.error("Stopping Simulation")
            sys.exit()
    

def main():
    try:
        if len(sys.argv) == 2:
            # tech = sys.argv[1]
            # rtlFile = sys.argv[2]
            # effortSet = sys.argv[3]
            # constraints = sys.argv[4]{self.filename_with_extension_top} 
            # format = sys.argv[5]
            topmodule = sys.argv[1]
            bottomModule = sys.argv[2]
            #Create instance
            sim  = Xcelium(topmodule, bottomModule)

            #Admin Job - For Logging
            sim.adminJob()

            #Change Directory
            sim.chngDir()
    
            # #Write TCL Script from Template
            # syn.writeTcl()

            # #Change Directory to New Directory
            # syn.tclDir()

            #Enter the Cadence shell and perform genus operation
            sim.xceliumFlow()

            #Writing Build Artifacts
            data = sim.generate_json_data()
            sim.save_json_data(data)
            
        else:
            logging.info("No Parameter Passed")
    except Exception as exception:
        logging.error(f"-----Exception: {exception}")
        logging.error(f"------Exiting Execution")
        sys.exit()
    return 0

if __name__ == '__main__':
    main()