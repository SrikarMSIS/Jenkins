
#This code is to be run as a part of the main code for the automation
#To change to the local directory, we use the Change_Directory class which then 
#branches to the subroutine class to initiate the cadence commands
#On completion of the cadence commands, the log file is use to check for any errors during the execution of the cadence commands
import os
import sys
import time
import glob
import shutil
from datetime import datetime
from subroutine_test import Subroutine


class Jenkins_Automation:
    def __init__(self):
        # TODO: Constructor
        self.currentPath = os.getcwd()
        self.newPath = None
        self.topModule = None
        self.bottomModule = None


    def admin_jobs(self):
        #Take inputs of the paths
        try:
            print("------------------------------------------------------")
            print("-----------Welcome to JENKINS AUTOMATION--------------")
            print("------------------------------------------------------")
            time.sleep(2)
            print("-- WE REQUEST YOU TO GO THROUGH THE FOLLOWING --")
            time.sleep(2)
            print("-- Please ensure that the top and bottom modules are in the same path")
            time.sleep(3)
            print("-- Please wait until the complete execution OR until prompted")
            print("------------------------------------------------------")
            time.sleep(3)
            print("-- Execution Commences")
            print("------------------------------------------------------")
            time.sleep(2)
            self.newPath = input("-- Please provide the path to the MODULES:\n")
            time.sleep(1)
            self.topModule = input("-- Please provide the file name of the top module with .v or .sv extension:\n")
            self.bottomModule = input("-- Please provide the file name of the bottom module with .v extension:\n")
        except Exception as exception:
            print("BRANCH: ADMIN JOB")
            print(f"ERROR : {exception}")
            print("-- Exiting Execution")
            sys.exit()
        return 0




    def enter_directory(self):
        os.chdir(self.newPath)
        return 0


    def exit_directory(self):
        os.chdir(self.currentPath)
        return 0


    def copy_vcd_log(self):
        #Copy the VCD and LOG file from cadence path to current path
        try:
            vcd_files = glob.glob(os.path.join((self.newPath),'*.vcd'))
            log_files = glob.glob(os.path.join((self.newPath),'*.log'))


            #Make a folder with name as present time
            current_time = datetime.now()
            formatted_time = current_time.strftime('%Y-%m-%d_%H-%M-%S')
            folder_name_split, folder_name_split_two = self.bottomModule.split(".",1)
            folder_name = "output_files_" + folder_name_split + "_" + formatted_time
            folder_path = os.path.join(self.currentPath,folder_name)
            os.makedirs(folder_path)


            #Copy the file into the folder
            for file in vcd_files[:1] + log_files[:1]:
                shutil.copy(file, folder_path)


        except Exception as exception:
            print("--BRANCH: COPYING INNER")
            print(f"ERROR: {exception}")
            print("-- EXITING EXECUTION")
            sys.exit()


        return 0


def main():


    #Creating instance of the class
    jenkins = Jenkins_Automation()


    #Function to perform admin work like taking input paths and output paths
    jenkins.admin_jobs()
    print("-- ADMIN Job execution successful")


    #Function to perform change directory job
    try:


        jenkins.enter_directory()
        print(f"Previously:{jenkins.currentPath}")
        print(f"Currently: {jenkins.newPath}")
        if jenkins.newPath == os.getcwd():
            print("-- Entered User Defined Path to execute Cadence Commands")
        else:
            print("-- Not able to branch to the User Defined Path")
            print("-- Exiting Execution")
            sys.exit()


    except Exception as exception:
        print("BRANCH: Change Directory JOB")
        print(f"ERROR : {exception}")
        print("-- Exiting Execution")
        sys.exit()




    #Function to call subroutine job
    try: 
        #Check if file exists in the path before providing to Cadence
        topFile = f"{jenkins.topModule}"
        bottomFile = f"{jenkins.bottomModule}"
        pathTop = glob.glob(os.path.join(jenkins.newPath,topFile))
        pathBottom = glob.glob(os.path.join(jenkins.newPath,bottomFile))
        if pathTop and pathBottom:
            Subroutine.sub_routine(jenkins.topModule, jenkins.bottomModule)
        else:
            print("-- Please Ensure That the top and bottom modules are in the same path")
            print("-- Exiting Execution")
            sys.exit()


    except Exception as exception:
        print("BRANCH: CADENCE JOB")
        print(f"ERROR : {exception}")
        print("-- Exiting Execution")
        sys.exit()


    #Function to copy the Log file and VCD file to the Main Directory before executing KPI Job
    try:
        jenkins.copy_vcd_log()


    except Exception as exception:
        print("BRANCH: COPY FILES JOB")
        print(f"ERROR : {exception}")
        print("-- Exiting Execution")
        sys.exit()


    #Function to exit the cadence directory after copying the files
    try:
        jenkins.exit_directory()


    except Exception as exception:
        print("BRANCH: EXIT DIRECTORY JOB")
        print(f"ERROR : {exception}")
        print("-- Exiting Execution")
        sys.exit()




if __name__ == "__main__":
    main()
