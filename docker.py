import os
import pexpect
import subprocess
import docker

def create_archive():
    os.system("tar -czf code.tar.gz ./*")

# Also need to enable SSH, ifconfig, python, etc
def create_attacker(client):
    base = client.images.pull("phusion/baseimage:latest")
    c = client.containers.run(base, "/sbin/my_init", detach=True)
    print(c.status)
    codebase = opne("code.tar.gz", "rb").read()
    c.put_archive("/", codebase)
    return c

def create_target(client):
    base = client.images.pull("phusion/baseimage:latest")
    c = client.containers.run(base, "/sbin/my_init", detach=True)
    print(c.status)
    return c

def run(container, command):
    print(container.exec_run(command))

create_archive()

client = docker.from_env()
b = create_attacker(client)
target = create_target(client)

