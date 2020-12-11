import sys
import getpass
import paramiko
from device_check import cdw_script_validator
import time
import os
from datetime import datetime

class run_command_on_bmn():
    setting_up_test = "FALSE"
    customer = ""
    username = ""
    password = ""
    cmd = ""
    devices = []
    device = ""
    ssh_opened = "False"
    session = ""
    device_utility = cdw_script_validator()
    ios = ""
    pytest = ""

   #Setting up the script to run
    def set_customer(self, cust):
        self.customer = cust

    def get_targets(self):
        f = open("CI-MASTER.csv","r")
        for line in f:
            split_line = line.split(",")
            customer_from_file = split_line[4].lower().replace("\n","").replace("","")
            if customer_from_file ==  self.customer.lower():
                self.devices.append(split_line)

        print("Total of {} images that will be tested on this BMN".format(len(self.devices)))

    def print_device_output(self, split_line):
        devices = split_line[0].split(".")
        device = devices[0]
        print("CI:\t{}".format(device.upper()))

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password

    def set_command(self, command):
        self.cmd = command

   #Dashboard
    devices_not_found = []
    def run_command_devices(self, run_name = ""):
        path = os.getcwd()
        now = datetime.now()
        i = 0
        try:
            folder_name = "PYTESTRUN_{}.{}.{}.{}.{}.{}".format(run_name, now.month, now.day, now.year, now.hour, now.minute)
            os.mkdir("{}/{}".format(path, folder_name))
        except OSError:
            print ("Creation of the directory %s failed" % path)
            sys.exit()
        else:
            print ("Successfully created the directory %s " % path)
        print ("The current working directory is %s" % path)
        Results_CSV= open("Results_{}.csv".format(run_name),"w+")
        for line in self.devices:
            results = "N/A"
            print(line)
            self.device = line[0]
            self.ios = line[3]
            if self.ssh_opened == "False":
                self.open_ssh_connection()
                self.device = self.device.split(".")
                ssh_output_host = self.run_command_ssh_with_open_connection(self.cmd)
                for line in ssh_output_host:
                    if "Invalid" in line:
                        results = "Invalid"
                        print("{} - {}".format(self.device,"INVALID"))
                        #continue

                if ssh_output_host != "Device not found":
                    file_output = "{}/{}-{}-output.text".format(folder_name,self.device[0], self.ios)
                    results = "OK"
                    f= open(file_output,"w+")
                    for line in ssh_output_host:
                        line.replace("\n","")
                        f.write("{}\n".format(line))
                else:
                    results = "Not found"
                    device_ios_pair = [self.device, self.ios]
                    self.devices_not_found.append(device_ios_pair)
                
                print("{} - {} - {}".format(self.device[0],self.ios, ssh_output_host))
                self.close_command_ssh()
                line_device = "{},{},{}\n".format(self.device[0],self.ios,results)
                print("***",line_device)
                Results_CSV.write(line_device)
        print("Device\t\t\t\tIOS")
        for line in self.devices_not_found:
            print("{}\t\t\t{}".format(line[0],line[1]))
   #SSH Interaction
    def open_ssh_connection(self):
        self.device_utility.debug_alerts("open_ssh_connection - Checking if connection is opened") 
        #print("Device: {}\tuser: {} \tPassword: {}".format(self.device,self.username, self.password))
        if self.ssh_opened == "False":
            self.device_utility.debug_alerts("open_ssh_connection - Connection is closed, opening") 
            #print("Open SSH")
            #print(self.device)
            #print("70 - ",self.device, self.username, self.password, "terminal length 0")
            self.output_interface_state = self.run_command_ssh_with_auth(self.device, self.username, self.password, arg_command="terminal length 0")
            self.ssh_opened = "True"

        elif self.ssh_opened == "True":
            self.device_utility.debug_alerts("open_ssh_connection - Connection is already opened, using opened connection") 

    def run_command_ssh_with_auth(self,device, arg_username, arg_password, arg_command=None):
        self.device_utility.debug_alerts("run_command_ssh_with_auth - Using paramiko to access the device, setting up paramiko.")
        self.session = paramiko.SSHClient()
        self.session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.device_utility.debug_alerts("run_command_ssh_with_auth - About to connect to the device.")

        try:    
            self.session.connect(device, username=arg_username, password=arg_password)

        except Exception as e:
            #MAKE A FUNCTION send e as an argument.
            self.device_utility.debug_alerts("run_command_ssh_with_auth - Error issues with Paramiko exception happened")
            if "Authentication failed" in str(e):
                self.device_utility.debug_alerts("run_command_ssh_with_auth - Authentication failed")
                if self.pytest == "True":
                    raise ValueError("Authentication Failed")
                else:
                    self.device_utility.debug_alerts("run_command_ssh_with_auth - Device is not reachable.")
                    self.device_utility.print_easy_banner("Authentication has failed please check credentials")
                    sys.exit()                
                    return "Authentication Failed"                    

            elif "Operation timed out" in str(e):
                self.device_utility.debug_alerts("run_command_ssh_with_auth - Operation timed out")
                if self.pytest == "True":
                    raise ValueError("Operation timed out")
                else:
                    self.device_utility.debug_alerts("run_command_ssh_with_auth - Device is not reachable.")
                    self.device_utility.print_easy_banner("Authentication has failed please check credentials")
                    sys.exit()                
                    return "Operation timed out" 

            elif "send" in str(e):
                self.device_utility.debug_alerts("run_command_ssh_with_auth - SEND")
                if self.pytest == "True":
                    raise ValueError("SEND")
                else:
                    self.device_utility.debug_alerts("run_command_ssh_with_auth - SEND.")
                    self.device_utility.print_easy_banner("SEND")
                    sys.exit()                
                    return "SEND" 

        self.device_utility.debug_alerts("run_command_ssh_with_auth - Invoking paramiko's shell.")
        try:
            self.connection = self.session.invoke_shell()
        except:
            return "Exception 123"
        
        self.device_utility.debug_alerts("run_command_ssh_with_auth - Run send command on paramiko.")
        self.connection.send("{}\n\n".format(arg_command))
        time.sleep(5)

        self.device_utility.debug_alerts("run_command_ssh_with_auth - Getting output to command_response.")        
        command_response = self.connection.recv(200000)
        command_response = command_response.decode('utf-8')
        command_response = command_response.split('\n')
        return command_response
            
    def run_command_ssh_with_open_connection(self,arg_command = None):
        self.device_utility.debug_alerts("run_command_ssh_with_open_connection - Running a command with an opened SSH connection.")
        if self.setting_up_test == "FALSE":
            try:
                self.connection.send("{}\n\n".format(arg_command))
            except:
                if self.pytest == "True":
                    raise ValueError("Error triggered with an opened connection")
                else:
                    self.device_utility.debug_alerts("run_command_ssh_with_auth - Device is not reachable.")
                    return "Device not found"
            time.sleep(5)
            command_response = self.connection.recv(200000)
            command_response = command_response.decode('utf-8')
            command_response = command_response.replace('\r','')
            command_response = command_response.split('\n')
            return command_response

    def close_command_ssh(self):
        self.device_utility.debug_alerts("close_command_ssh - Clossing the SSH Connection.")        
        self.connection.close()
        self.ssh_opened = "False"

if __name__ == "__main__":
    cls_command = run_command_on_bmn()
    print("Input a username that will be used multiple times.\n\n")
    user = input("Username:")
    pwd = getpass.getpass("Password:")
    cmd = input("Command to run thru all the devices:")
    folder = input("Type name of run")
    cls_command.set_customer("REYES")
    cls_command.get_targets()
    cls_command.set_username(user)
    cls_command.set_password(pwd)
    cls_command.set_command(cmd)
    cls_command.run_command_devices(run_name = folder)
