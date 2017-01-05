import os
import pexpect
import subprocess
import docker
import sys
import random

from colorama import *

GOOD = Fore.GREEN + " + " + Fore.RESET
BAD = Fore.RED + " - " + Fore.RESET
WARN = Fore.YELLOW + " * " + Fore.RESET
INFO = Fore.BLUE + " + " + Fore.RESET


class Machine(object):
    def __init__(self, image="phusion/baseimage:latest", verbose=True):
        self.image = image
        self.client = docker.from_env()
        self.base = self.client.images.pull(self.image)
        self.container = self.client.containers.run(self.base, "/sbin/my_init", detach=True) 
        self.verbose = verbose
        self.docker_id = str(self.container.id[:12])

    def stop(self):
        return self.container.stop()

    def get_status(self):
        return self.container.status

    def run(self, command):
        if self.verbose:
            print("# " + command)
        res = self.container.exec_run(command)
        if self.verbose:
            print(res)
        return res
    
    def get_ip(self):
        return self.run("ifconfig eth0 | grep \"inet \"  | awk -F'[: ]+' '{ print $4 }'")

def create_archive():
    os.system("tar -czf code.tar.gz ./* 2> /dev/null")

def setup_attacker(m):
    codebase = open("code.tar.gz", "rb").read()
    m.container.put_archive("/", codebase)
    m.run("apt-get update")
    m.run("apt-get install -y netcat nmap git ssh libssl-dev python-tk python-dev python-pip build-essential libxml2-dev libxslt1-dev zlib1g-dev")
    return True

def setup_target(m):
    m.run("apt-get update")
    m.run("useradd -ms /bin/bash george")
    m.run("echo 'george:password' | chpasswd")
    m.run("apt-get install -y openssh-server ssh net-tools netcat python")
    m.run("service ssh start")
    return True

'''
machines = {}
client = docker.from_env()
create_archive()

try:
    print(GOOD + "Creating attacker...")
    machines["Attacker"] = Machine()
    print(GOOD + "Setting up attacker...")
    setup_attacker(machines["Attacker"])

    print(GOOD + "Creating target...")
    machines["Target"] = Machine()
    print(GOOD + "Setting up target...") 
    setup_target(machines["Target"])     
    machines["Attacker"].run("python dependencies.py")
    input("")

finally:
    print(GOOD + "Cleaning up...")
    for m in machines:
        machines[m].stop()
'''
