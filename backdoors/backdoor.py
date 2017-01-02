import os
import cmd
from .option import *
from definitions import *
import math
import shlex
import importlib
import inspect
import sys
import multiprocessing
from six.moves import input
import socket
import time
import pexpect
import traceback
from connection import Connection

class Backdoor(cmd.Cmd):
    def __init__(self, core):
        super(Backdoor, self).__init__()
        self.options = {}
        self.core = core
        self.target = core.curtarget
        self.modules = {}
        self.allow_modules = True
        self.help_text = None
        self.listening = 0
        self.intro = ""
     
    def check_added(self, name):
        for m, opts in  self.modules.items():
            if m.name.lower() == name.lower():
                return m
        return None

    def complete_add(self, text, line, begin_index, end_index):
        return [item for item in self.walk("modules/", echo=False) if item.startswith(text)]
    
    def do_add(self, line):
        if self.allow_modules:
            for m in line.split():
                mod = self.check_added(m)
                if mod != None:
                   print(INFO + mod.name + " module already added.") 
                   continue
                try:
                    mod = importlib.import_module("modules." + m)
                    clsmembers = inspect.getmembers(sys.modules["modules."+m], inspect.isclass)
                    try:
                        mod = [c for c in clsmembers if c[1].__module__ == "modules."+m][0][1](self.core.curtarget, self, self.core)
                        self.modules[mod] = mod.options
                        print(GOOD + mod.name + " module added.")
                    except Exception as e:
                        #traceback.print_exc()
                        print(BAD + "An unexpected error occured.")
                except Exception as e:
                    #traceback.print_exc()
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

    def set_target(self, target):
        self.options['target'] = target

    def set_option(self, option, value):
        if option in self.options.keys():
            self.options[option] = value
            return True
        else:
            return False

    def do_exploit(self):
        return False

    def listen(self, passw="none", prompt="some"):
        self.child = pexpect.spawn("python listen.py " + str(self.get_value("port")) + " " + str(passw) + " " + str(prompt))
        time.sleep(.25)
        self.core.curtarget.sessions.append(Connection(self.intro, self.child))
        print("Session " + str(len(self.core.curtarget.sessions)) + " created")
        self.listening = 1

    def do_sessions(self, args):
        if args == "" or args == "--help" or args == "-h":
            print("Use sessions -l to list and sessions -i <num> to interact with a shell")
        if args == "" or args == "--list" or args == "-l":
            i = 1
            for session in self.core.curtarget.sessions:
                print(str(i))
                print(session)
                i += 1
        if "-i" in args or "--interact" in args:
            self.core.curtarget.sessions[int(args.split(" ")[1]) - 1].interact()

        print(args)

    def do_show(self, args):
        if args == "options":
            self.do_help(args)
        elif args == "modules":
            self.mods()
        else:
            print(BAD + "Unknown option %s", args)
    
    def do_set(self, args):
        args = shlex.split(args)
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
        print("")
        return True

    def emptyline(self):
        return

    def precmd(self, line):
        self._hist += [ line.strip() ]
        return line

    def do_history(self, args):
        print(self._hist)

    def default(self, line): 
        self.core.onecmd(line)

    def do_quit(self, args):
        print("Exiting")
        exit()

    def print_help(self, options):
        if options == {}:
            return
        vals = [str(o.value) for o in options.values()]
        l = int(math.ceil(max(map(len, vals)) / 10.0)) * 10
        print(("{0:<15} {1:<%s} {2:<30}" % str(l)).format("Option","Value", "Description"))
        print("="*(l+45))
        for name, opt in options.items():
            print(("{0:<15} {1:<%s} {2:<30}" % str(l)).format(opt.name, opt.value, opt.description))

    def do_help(self, args):
        if self.help_text is not None and self.help_text != "":
            print(self.help_text)
        print("Backdoor options: ")
        print("")
        self.print_help(self.options) 
        if self.allow_modules:
            print("")
            if self.modules != {}:
                for mod, opts in self.modules.items():
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
                if mod is not None:
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

    def walk(self,folder,echo=True):
        ms = []
        if echo:
            print(INFO + "Modules:")
        for root, dirs, files in os.walk(folder):
            del dirs[:] # walk down only one level
            path = root.split('/')
            for file in files:
                if file[-3:] == ".py":
                    ms.append(str(file).replace(".py", ""))
                    if echo:
                        print((len(path)*'  ') + "-", str(file).replace(".py", ""))
        return ms
