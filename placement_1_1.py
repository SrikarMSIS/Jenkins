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

class Placement:
    #Constructor
    def __init__(self, tech, pnrPath):
        self.tech = tech
        self.pnrPath = pnrPath
        self.placementTCL = "/home/vlsi/srikar/jenkins_auto/Jenkins/Jenkins/Scripts/TCL/placement_2_1.tcl"
        self.placeTCL = None

    
    def adminJob(self):
        """
        This function is used to execute the admin printing jobs

        Inputs: Self
        Returns: None
        
        """
        try:
            logging.info("----WELCOME TO JENKINS AUTOMATION")
            logging.info("----RUNNING PLACEMENT")
            logging.info(f"Technology : {self.tech}")
            logging.info(f"PNR Path : {self.pnrPath}")
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
            logging.info(f"Changing to: {self.pnrPath}")
            os.chdir(self.pnrPath)

        except Exception as exception:
            logging.error(f"--Exception Incurred: {exception}")
            logging.error("Exiting Simulation")
            sys.exit()
        return 0
    
    
    @staticmethod
    def createPlacementTcl(content, path):
        """
        This function takes the TCL Content and then write it to the new path
        Inputs: TCL Content, self.pnrPath
        Returns: New TCL Script Path

        """
        try:
            tclFileName = "place.tcl"
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
            if(os.path.exists(self.pnrPath)):
                #Open the template in read and write mode and write the modified content
                with open(self.placementTCL, 'r') as file:
                    placeContent = file.read()
                modContents = placeContent.replace('{tech}',self.tech)
                self.placeTCL = self.createPlacementTcl(modContents, self.pnrPath)

                
        except Exception as exception:
            logging.error(f"---Exception Occured: {exception}")
            logging.error("Exiting Simulation")       
            sys.exit()
        return 0
    
    def placeFlow(self):
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
            source_cmd = 'sudo -u vlsi csh -c "source /home/install/cshrc && innovus -stylus -file place.tcl"'
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
            "path" : self.pnrPath,
            "placement_path" : self.pnrPath
        }

        return data
    
    def save_json_data(self, data):
        try:
            self.artifact_filepath = os.path.join(self.pnrPath, "synth_build_info.json")
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
            pnrFolder = sys.argv[2]
    
            #Create instance
            plc = Placement(tech, pnrFolder)

            # #Admin Job - For Logging
            plc.adminJob()

            #Change Directory
            plc.chngDir()

            # #Write TCL Script from Template
            plc.writeTcl()

            # #Enter the Cadence shell and perform genus operation
            plc.flpFlow()

            data = plc.generate_json_data()
            plc.save_json_data(data)
            json_file_path = plc.artifact_filepath
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
