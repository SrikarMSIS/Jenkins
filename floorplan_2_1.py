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
    def __init__(self, tech, synFiles, moduleName):
        self.logPath = "/home/vlsi/srikar/jenkins_auto"
        self.synFiles = synFiles
        self.technology = tech
        self.flp_path = None
        self.reqJson = "/home/vlsi/srikar/jenkins_auto/Jenkins/Jenkins/Scripts/JSON/required.json"
        self.lib = None
        self.libMin = None
        self.tech_lef = None
        self.macro_lef = None
        self.capMax = None
        self.capMin = None
        self.qrc = None
        self.mmmcTcl = "/home/vlsi/srikar/jenkins_auto/Jenkins/Jenkins/Scripts/TCL/mmmc_1_2.tcl"
        self.floorplanTcl = "/home/vlsi/srikar/jenkins_auto/Jenkins/Jenkins/Scripts/TCL/floorplan_2_1.tcl"
        self.sdc= None
        self.mmmcPath = None
        self.moduleName = moduleName
        self.netlist =None

    
    def adminJob(self):
        """
        This function is used to execute the admin printing jobs

        Inputs: Self
        Returns: None
        
        """
        try:
            logging.info("----WELCOME TO JENKINS AUTOMATION")
            logging.info("----RUNNING FLOORPLAN")
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
        Copy the netlist.v and block.sdc file 
        
        Inputs: Self
        Returns: None

        """
        try:
            logging.info("----Changing the Working Path")
            logging.info(f"Changing to: {self.synFiles}")
            os.chdir(self.synFiles)
            flp_folder_name = "pnr"
            flp_folder_path = os.path.join(self.synFiles,flp_folder_name)
            os.makedirs(flp_folder_path)
            if(os.path.exists(flp_folder_path)):
                logging.info("---PNR Folder created")
                os.chdir(flp_folder_path)
                self.flp_path = flp_folder_path
                logging.info(f"--Working in {self.flp_path}")
                #Copy the netlist.v and block.sdc files to the current path
                synthName = "synthesis"
                netlistSDC = os.path.join(self.synFiles, synthName)
                if(os.path.exists(netlistSDC)):
                    logging.info("---Synthesis Folder Exists")
                    netlist = "netlist.v"
                    constraints = "block.sdc"
                    netlistPath = os.path.join(netlistSDC, netlist)
                    constPath = os.path.join(netlistSDC, constraints)
                    shutil.copy(netlistPath, self.flp_path)
                    shutil.copy(constPath, self.flp_path)
                    self.sdc = os.path.join(self.flp_path, constraints)
                    self.netlist = os.path.join(self.flp_path, netlist)
                else:
                    logging.warning("Synthesis Folder not visible")
                    sys.exit()
            else:
                logging.error("--PNR Folder Not Created")
                sys.exit()

        except Exception as exception:
            logging.error(f"--Exception Incurred: {exception}")
            logging.error("Exiting Simulation")
            sys.exit()
        return 0
    
    @staticmethod
    def createmmmcTcl(content, path):
        """
        This function takes the TCL Content and then write it to the new path
        Inputs: TCL Content, self.flpPath
        Returns: New TCL Script Path

        """
        try:
            tclFileName = "mmmc.tcl"
            tclPath = os.path.join(path, tclFileName)
            with open(tclPath, 'w') as file:
                file.write(content)
            logging.info(f"TCL Script Written in the path: {tclPath}")
        
        except Exception as exception:
            logging.info(f"---Exception: {exception}")
            logging.info("---Stopping Execution")
            sys.exit()
        
        return tclPath
    
    @staticmethod
    def createflpTcl(content, path):
        """
        This function takes the TCL Content and then write it to the new path
        Inputs: TCL Content, self.synthPath
        Returns: New TCL Script Path

        """
        try:
            tclFileName = "flp.tcl"
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

                self.lib = jsonData[self.technology]["Floorplan"]["lib"]
                self.libMin = jsonData[self.technology]["Floorplan"]["libMin"]
                self.capMax = jsonData[self.technology]["Floorplan"]["capTableMax"]
                self.capMin = jsonData[self.technology]["Floorplan"]["capTableMin"]
                self.qrc = jsonData[self.technology]["Floorplan"]["qrcTech"]
                self.tech_lef = jsonData[self.technology]["Floorplan"]["tech_lef"]
                self.macro_lef = jsonData[self.technology]["Floorplan"]["macro_lef"]

                #Open the template in read and write mode and write the modified content
                with open(self.mmmcTcl, 'r') as file:
                    mmmcContent = file.read()
                modContents = mmmcContent.replace('{libMin}',self.libMin).replace('{lib}',self.lib).replace('{qrc}',self.qrc).replace('{capMin}',self.capMin).replace('{capMax}',self.capMax).replace('{sdc}',self.sdc)
                self.mmmcPath = self.createmmmcTcl(modContents, self.flp_path)

                with open(self.floorplanTcl, 'r') as file:
                    flpContent = file.read()
                modContents = flpContent.replace('{module}', self.moduleName).replace('{tech_lef}', self.tech_lef).replace('{macro_lef}',self.macro_lef).replace('{netlist}', self.netlist).replace('{mmmc_path}', self.mmmcPath)
                self.flpTclPath = self.createflpTcl(modContents, self.flp_path)

                
        except Exception as exception:
            logging.error(f"---Exception Occured: {exception}")
            logging.error("Exiting Simulation")       
            sys.exit()
        return 0
    
    def flpFlow(self):
        """
        This function is used to enter the cadence shell and invoke the Innovus Stylus tool.
        Once invoked, the tool will run on the TCL file created previously.
        Inputs: Self
        Returns: None

        """
        try:
            logging.info("---------------")
            logging.info("--Entering the Cadence Shell")
            logging.info("---------------")
            source_cmd = 'sudo -u vlsi csh -c "source /home/install/cshrc && innovus -stylus -file flp.tcl"'
            subProcess = subprocess.Popen(source_cmd ,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
            stdout, stderr = subProcess.communicate()
            logging.info(f"Floorplan Output: {stdout}")
            logging.error(f"Floorplan Error: {stderr}")
            logging.info("--Floorplan Done")
        
        except Exception as exception:
            logging.error(f"!Execption: {exception}")
            logging.error(f"Stopping Simulation")
            sys.exit()

        return 0
    
    def generate_json_data(self):
        data = {
            "build_number" : os.environ.get("BUILD_NUMBER"),
            "path" : self.flp_path,
            "floorplan_path" : self.flp_path
        }

        return data
    
    def save_json_data(self, data):
        try:
            self.artifact_filepath = os.path.join(self.flp_path, "synth_build_info.json")
            with open(self.artifact_filepath, 'w') as file:
                json.dump(data, file, indent=4)

            print(self.artifact_filepath)

            if os.path.exists(self.artifact_filepath):
                logging.info(f"JSON file successfully written to: {self.artifact_filepath}")
                return self.artifact_filepath # Return the path only if the file exists
            else:
                logging.error(f"Error: JSON file not found after writing! Path: {self.artifact_filepath}")
                sys.exit(1) # Exit with an error code if the file doesn't exist
            
            
        
        except Exception as exception:
            logging.error(f"Exception: {exception}")
            logging.error("Stopping Simulation")
            sys.exit()

        return 0


def main():
    try:
        if len(sys.argv) > 1:
            tech = sys.argv[1]
            synFolder = sys.argv[2]
            moduleName = sys.argv[3]
    
            #Create instance
            flp = Floorplan(tech, synFolder, moduleName)

            # #Admin Job - For Logging
            flp.adminJob()

            #Change Directory
            flp.chngDir()

            # #Write TCL Script from Template
            flp.writeTcl()

            # #Enter the Cadence shell and perform genus operation
            flp.flpFlow()

            data = flp.generate_json_data()
            flp.save_json_data(data)
            json_file_path = flp.artifact_filepath
            print(f"JSON FIle Path = {json_file_path}")
        else:
            logging.info("No Parameter Passed")
            
    except Exception as exception:
        logging.error(f"-----Exception: {exception}")
        logging.error(f"------Exiting Execution")
        sys.exit()
    return 0

if __name__ == '__main__':
    main()
