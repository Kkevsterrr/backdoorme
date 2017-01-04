import cmd
import os
from colorama import *
from .option import *

GOOD = Fore.GREEN + " + " + Fore.RESET
BAD = Fore.RED + " - " + Fore.RESET
WARN = Fore.YELLOW + " * " + Fore.RESET
INFO = Fore.BLUE + " + " + Fore.RESET

class Module(object):
    def __init__(self, core):
        self.options = {}
        self.core = core
    
    def set_option(self, option, value):
        if option in self.options.keys():
            self.options[option] = value
            return True
        else:
            return False

    def get_value(self, name):
        if name in self.options:
            return self.options[name].value
        else:
            return None

    def help(self, args):
        for name, opt in self.options.items():
            print("%s\t\t%s\t\t%s\t\t%s" % (opt.name, opt.value, opt.description, opt.required))
