import time
import sys
import os
import subprocess
class Subroutine:
    def sub_routine(topModule, bottomModule):
        """
        Method to run XRUN, read and represent the VCD file in a clean format

        Inputs: None
        Outputs: None

        """
        try:
            print("------------------------------------")
            print("-- Inside the Subroutine function")
            print("------------------------------------")
            print("-- Entering the cadence shell")
            print("------------------------------------")
            time.sleep(2)
            print("-- Executing in the following path")
            print(f"{os.getcwd()}")
            source_cmd = "source /home/installs/cshrc"
            xrun_cmd = f"xrun +access+rwc {topModule} {bottomModule}"
            subProcess = subprocess.Popen(['/bin/csh', '-i'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            subProcess.stdin.write(f"{source_cmd}\n".encode())
            subProcess.stdin.write(f"{xrun_cmd}\n".encode())
            subProcess.stdin.write("exit\n".encode())
            output, error = subProcess.communicate()
            print(output.decode('utf-8'))

        except Exception as exception:
            print("BRANCH: CADENCE SUBROUTINE JOB")
            print(f"ERROR : {exception}")
            print("-- Exiting Execution")
            sys.exit()

        #Subroutine.cadence_shell()
        return 0


