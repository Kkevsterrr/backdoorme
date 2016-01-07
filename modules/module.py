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

    def do_show(self, args):
        if args == "options":
            self.do_help(args)
        else:
            print BAD + "Unknown option %s", args
    
    def do_set(self, args):
        args = args.split(" ")
        if len(args) == 2 and args[0] in self.options:
            self.options[args[0].lower()].value = args[1]
            print "%s => %s" % (args[0], args[1])
        elif len(args) != 2:
            print "Please supply a variable and an option"
            print "Usage: set LHOST 10.1.0.1"
        else:
            print BAD + "Unknown option %s", args[0]

    def get_value(self, name):
        if name in self.options:
            return self.options[name].value
        else:
            return None

    def do_help(self, args):
        for name, opt in self.options.iteritems():
            print("%s\t\t%s\t\t%s\t\t%s" % (opt.name, opt.value, opt.description, opt.required))
