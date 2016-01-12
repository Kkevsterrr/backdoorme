import cmd
from option import *
import os
import cmd
from colorama import *
from definitions import *

class Backdoor(object, cmd.Cmd):
    def __init__(self, core):
        self.options = {}
        self.core = core
        self.modules = {}
        self.allow_modules = True
        self.help_text = None

    def check_valid(self):
        return False
    
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
    def do_help(self, args):
        if self.help_text != None and self.help_text != "":
            print self.help_text
        print "Backdoor options: "
        print("")
        print "Option\t\tValue\t\tDescription\t\tRequired"
        print "------\t\t-----\t\t-----------\t\t--------"
        for name, opt in self.options.iteritems():
            print("%s\t\t%s\t\t%s\t\t%s" % (opt.name, opt.value, opt.description, opt.required))
        if self.allow_modules:
            if self.modules != {}:
                for mod, opts in self.modules.iteritems():
                    print("\n%s module options: \n" % mod.name)
                    print "Option\t\tValue\t\tDescription\t\tRequired"
                    print "------\t\t-----\t\t-----------\t\t--------"
                    for name, opt in mod.options.iteritems():
                        print("%s\t\t%s\t\t%s\t\t%s" % (opt.name, opt.value, opt.description, opt.required))
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


