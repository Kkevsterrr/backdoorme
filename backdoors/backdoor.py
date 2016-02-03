import cmd
from option import *
import os
import cmd
from colorama import *
from definitions import *
import subprocess
import math

class Backdoor(object, cmd.Cmd):
    def __init__(self, core):
        self.options = {}
        self.core = core
        self.modules = {}
        self.allow_modules = True
        self.help_text = None

    def check_valid(self):
        return False
   
    def complete_add(self, text, line, begin_index, end_index):
        return [item for item in self.core.enabled_modules.keys() if item.startswith(text)]

    def do_add(self, line):
        if self.allow_modules:
            for m in line.split():
                if m in self.core.enabled_modules.keys():
                    mod = self.core.enabled_modules[m](self.core.curtarget, self, self.core)
                    self.modules[mod] = mod.options
                    print(GOOD + mod.name + " module added.")
                else:
                    print(BAD + "No module \""+m+"\" available.")
        else:
            print(BAD + "Modules disabled by this backdoor.")

    def complete_set(self, text, line, begin_index, end_index):
        line = line.rsplit(" ")[1]
        segment = line.split(".")
        if len(segment) == 1:
            return [item for item in ([m.name.lower() for m in self.modules.keys()] + ["target"] + self.options.keys()) if item.startswith(text)]
        if len(segment) == 2:
            return [(segment[0] + "." + item) for item in self.get_by_name(segment[0]).options.keys() if item.startswith(text.replace(segment[0]+".",""))]

    def set_target(target):
        self.options['target'] = target

    def set_option(option, value):
        if option in self.options.keys():
            self.options[option] = value
            return True
        else:
            return False

    def do_exploit():
        return False

    def do_show(self, args):
        if args == "options":
            self.do_help(args)
        elif args == "modules":
            self.mods()
	else:
            print BAD + "Unknown option %s", args
    
    def do_set(self, args):
        args = args.split(" ")
        bad_opt = BAD + "Unknown option %s" % args[0]
        if len(args) == 2 and args[0] in self.options:
            self.options[args[0].lower()].value = args[1]
            print(GOOD + "%s => %s" % (args[0], args[1]))
        elif args[0] == "target":
            self.core.do_set(" ".join(args))
        elif len(args) != 2:
            print(BAD + "Usage: \"set <OPTION> <VALUE>\"")
        elif "." in args[0] and self.check_by_name(args[0].split(".")[0]):
            mod = args[0].split(".")[0]
            option = args[0].split(".")[1]
            module = self.get_by_name(mod)
            if module != None and option in module.options.keys():
               module.options[option].value = args[1]
               print(GOOD + "%s => %s" % (args[0], args[1]))
            else:
                print(bad_opt)
        else:
            print(bad_opt)

    def get_value(self, name):
        if name in self.options:
            return self.options[name].value
        else:
            return None
    def check_by_name(self, name):
        for mod in self.modules:
            if name.lower() == mod.name.lower():
                return True
        return False
    def do_EOF(self, line):
        print ""
        return True
    def emptyline(self):
        return
    def precmd(self, line):
        self._hist += [ line.strip() ]
        return line 
    def do_history(self, args):
        print self._hist
    def default(self, line): 
        self.core.onecmd(line)
    def do_quit(self, args):
        print "Exiting"
        exit()
    def print_help(self, options):
        if options == {}:
            return
        vals = [str(o.value) for o in options.values()]
        l = int(math.ceil(max(map(len, vals)) / 10.0)) * 10
        print(("{0:<15} {1:<%s} {2:<30}" % str(l)).format("Option","Value", "Description"))
        print "="*(l+45)
        for name, opt in options.iteritems():
            print(("{0:<15} {1:<%s} {2:<30}" % str(l)).format(opt.name, opt.value, opt.description))

    def do_help(self, args):
        if self.help_text != None and self.help_text != "":
            print self.help_text
        print "Backdoor options: "
        print("")
        self.print_help(self.options) 
        if self.allow_modules:
            print("")
            if self.modules != {}:
                for mod, opts in self.modules.iteritems():
                    print("\n%s module options: \n" % mod.name)
                    self.print_help(mod.options)
    def get_by_name(self, name):
        for mod in self.modules.keys():
            if mod.name.lower() == name.lower():
                return mod
        return None
    def do_remove(self, line):
        if self.allow_modules:
            for m in line.split():
                mod = self.get_by_name(m) 
                if mod != None:
                    self.modules.pop(mod, None)
                    print(GOOD + "Removed %s module." % m)
                else:
                    print(BAD + "No module \""+m+"\" enabled")
        else:
            print(BAD + "Modules disabled by this backdoor.")

    def preloop(self):
        cmd.Cmd.preloop(self)   ## sets up command completion
        self._hist    = []      ## No history yet
        self._locals  = {}      ## Initialize execution namespace for user
        self._globals = {}


