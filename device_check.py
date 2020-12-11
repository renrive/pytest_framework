import subprocess
import sys
import os
import subprocess
import sys
import re
import pprint

class cdw_script_validator:
    device_IP = ""
    device_status = ""
    pytest = "False"
    debugging = "No"
    screen_size = 190

    def set_device_to_validate(self, device):
        ping_device = f"ping {device} -c 2"
        try:
            self.debug_alerts("About run: {}".format(str(ping_device)))
            ping_output = subprocess.run(ping_device,shell=True,capture_output=True)
            #print(ping_output)
        except subprocess.CalledProcessError:
            self.debugging("Error on ping, raising error")
            raise SystemExit(f"ERROR running subprocess in VerifyUserInput Class")
        ping_output = ping_output.stdout.decode('utf-8').split('\n')
        #print(ping_device)
        self.device_status, self.device_IP = self.get_ip(ping_output)

    def get_ip(self, ping_output):
        device_found = "False"
        for line_output in ping_output:
            if "icmp_seq" in line_output:
                ping_line = line_output.split()
                for line in ping_line:
                    line = line.replace("(","")
                    line = line.replace(")","")
                    line = line.replace(":","")
                    line = line.replace(" ","")
                    regex = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
                    if not re.match(regex,line) == None:
                        #print("IP: {}".format(line))
                        return "REACHABLE", line
        if device_found == "False":
            return "UNREACHABLE", "NO IP FOUND"

 #Visual Aid
    def print_easy_banner(self, message):
        self.print_divider()
        self.print_dashboard_empty_divider(1)
        self.print_header(message, 1)
        self.print_dashboard_empty_divider(1)
        self.print_divider()
  
  #Prints a divider of asterisk on the first and last spaces of the line, to give the impression of a border of asterisks.
    def print_divider(self):
        print("*"*self.screen_size)

    def print_dashboard_empty_divider(self,asterisk):
        print(("*"*(asterisk)) + (" "*(self.screen_size - ((asterisk)*2))) + ("*"*(asterisk)))

    def print_header(self, phrase,asterisk):
        phrase = phrase.rstrip()
        phrase = phrase.lstrip()
        space = ((self.screen_size - ((asterisk)*2))  - len(phrase))/2
        print("{}{}{}{}{}".format(("*"*(asterisk))," "* int(space), phrase," "* int(space),"*"*(asterisk)))

    def print_line_left(self, phrase,spaceL):
        phrase = phrase.rstrip()
        phrase = phrase.lstrip()
        blank_left = " "*spaceL
        blank_right = " "*(self.screen_size - len(phrase)- spaceL - 2)
        line = "*{}{}{}*".format(blank_left,phrase.rstrip(), blank_right)
        print(line)

    def print_line_left_with_blank_space(self, phrase,spaceL):
        blank_left = " "*spaceL
        blank_right = " "*(self.screen_size - len(phrase)- spaceL - 2)
        line = "*{}{}{}*".format(blank_left,phrase.rstrip(), blank_right)
        print(line)

    def get_cell_blank(self, phrase, cell_size):
        final_cell_size = cell_size - len(phrase)
        final_phrase = "{}{}".format(phrase," "*final_cell_size)
        return final_phrase

 #Validations 
    def validate_empty(self, string, ErrorMessage, sys_exit = None):
        if string == "":
            if self.pytest == "True":
                raise ValueError(ErrorMessage)
            else:
                self.print_divider()
                self.print_dashboard_empty_divider(1)
                self.print_header(ErrorMessage,1)
                self.print_dashboard_empty_divider(1)
                self.print_divider()
                if sys_exit == "True":
                    sys.exit()
            return "False"
        else:
            return "True"

    def validate_empty_spaces(self, string, ErrorMessage, sys_exit = None):
        if " " in string:
            if self.pytest == "True":
                raise ValueError(ErrorMessage)
            else:
                self.print_divider()
                self.print_dashboard_empty_divider(1)
                self.print_header(ErrorMessage,1)
                self.print_dashboard_empty_divider(1)
                self.print_divider()
                if sys_exit == "True":
                    sys.exit()                
            return "False"
        else:
            return "True"

    def validate_regex(self, string,regex, ErrorMessage, sys_exit = None):
        #print("REGEX: {}\t\tSTRING:{}\t\tRESULT:{}:".format(regex,string,re.match(regex,string) ))
        if re.match(regex,string) == None:            
            if self.pytest == "True":
                raise ValueError(ErrorMessage)
            else:
                self.print_divider()
                self.print_dashboard_empty_divider(1)
                self.print_header(ErrorMessage,1)
                self.print_dashboard_empty_divider(1)
                self.print_divider()
                if sys_exit == "True":
                    sys.exit()                
            return "False"     
        else:
            return "True"   

 #Error handling and alerts
    def debug_alerts(self, debug_message, sys_exit = None):
        if self.debugging == "Yes":
            print("**\t{}".format(debug_message))

    def Raise_Error(self, error_message, sys_exit = None):
        if self.pytest == "True":
            raise ValueError(error_message)

        else:
            self.print_easy_banner(error_message)

        if sys_exit == "Yes":
            sys.exit()



