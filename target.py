from paramiko import SSHClient
from scp import SCPClient
import paramiko
import os
import socket
import subprocess
from definitions import *

class Target:
    def __init__(self, hostname, uname, pword, num, port=22):
        self.hostname = hostname
        self.uname = uname
        self.pword = pword
        self.target_num = num
        self.port = port
        self.ssh = None 
        self.is_open = False 
        self.scp = None   
    def conn(self):
        #print("Opening SSH connection to target...")
        self.ssh = paramiko.SSHClient()#use ssh.exec_command("") to perform an action.
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.hostname, port=self.port, username=self.uname, password=self.pword)
        self.scp = SCPClient(self.ssh.get_transport())#don't call this, but use the above function instead.
        self.is_open = True
    #TODO: fix rm -rf bug
    def scpFiles(self, filename,a, recur=True):#call this with a filename and false if it is a single file
        print(GOOD + "Shipping files: ")
        print(INFO + a)
        bareFile = ""
        for i in range(len(a)-1, 0, -1):
            if(a[i] == '/'):
                break;
            else:
                bareFile += a[i]
        bareFile = bareFile[::-1]
        #print bareFile
        #print("echo " + self.pword + " | sudo -S rm " + bareFile)
        self.ssh.exec_command("echo " + self.pword + " | sudo -S rm " + bareFile)
        self.scp.put(a, recursive=recur)
    
    def close(self):
        self.is_open = False
        self.ssh.close()


