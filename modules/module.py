import cmd
from option import *
from definitions import *
import os

class Module(object):
    def __init__(self, core):
        self.options = {}
        self.core = core
    
    def set_option(option, value):
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
        for name, opt in self.options.iteritems():
            print("%s\t\t%s\t\t%s\t\t%s" % (opt.name, opt.value, opt.description, opt.required))
