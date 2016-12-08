#This is a template for your use to add additional modules. Modules are used to make a backdoor more potent, stealthy, or dangerous, but feel free to add anything you think might help! Places you need to input are designated by ~tildes~.
from .module import *

class ~NAME~(Module):
    def __init__(self, target, command, core):
        self.core = core
        self.target = target
        self.name = "~NAME~"
        self.command = command
        self.options = { #~Add options to make your module more potent.~
        }

    def exploit(self):
        #~ADD YOUR INSTRUCTIONS HERE. If you need th command, it is self.backdoor.get_command().~
        print(GOOD + self.name + " module success")

#Please add this to the backdoorme/modules/__init__.py file following the established convention.
