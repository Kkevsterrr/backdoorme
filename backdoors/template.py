#This is the template to create backdoors. Please copy your backdoor into the suggested spots. Places you need to input are shown by ~tildes~.
from backdoor import *
#Remember extra imports.

class ~NAME~(Backdoor):
    prompt = Fore.RED + "~NAME~" + Fore.BLUE + ">> " + Fore.RESET

    def __init(self, core):
	cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using ~NAME~ module..."
        self.core = core
        self.options = { #~Input extra options. You almost always need a port.~
                }
        self.allow_modules = True
        self.modules = {}
        self.help_text = ""

    def get_command(self):
	#~Add the final command.~

    def do_exploit(self, args):
	#~Add all commands needed to run the program.~

#After you have filled out this entire program, move it to the correct folder. 



