from backdoors.backdoor import *

#First argument - port 
#Second argument - password
#third - if it has a prompt or not, defaults to some (meaning it has a prompt)

class Listen(Backdoor):
    prompt = Fore.RED + "(Listener) " + Fore.BLUE + ">> " + Fore.RESET

    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using Listener module..."
        self.core = core
        self.options = {
                "port"   : Option("port", 53923, "port to begin the listener on", True),
                "password": Option("password", "none", "password for the connection", True),
                "prompt": Option("prompt", "none", "prompt for the shell", True)
                }
        self.allow_modules = False
        self.modules = {} 
        self.help_text = INFO + "Create a listener for a backdoor"

    def do_exploit(self, args):
        print(GOOD + "Initializing listener...")
        self.listen(str(self.get_value("password")), str(self.get_value("prompt")))

