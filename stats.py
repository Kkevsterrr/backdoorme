from master import *
from nose.tools import nottest
import pexpect
import random
import sys
from containers import *

NUM_TESTS = 5
PASSRATE = 0.9
DOCKER = False

@nottest
def setup():
    if DOCKER:
        machines = {}
        client = docker.from_env()
        create_archive()

        print(GOOD + "Creating attacker...")
        machines["Attacker"] = Machine()
        print(GOOD + "Setting up attacker...")
        setup_attacker(machines["Attacker"])

        print(GOOD + "Creating target...")
        machines["Target"] = Machine()
        print(GOOD + "Setting up target...") 
        setup_target(machines["Target"])     
        machines["Attacker"].run("python dependencies.py")
        print(machines["Target"].get_ip()) 
        return machines, machines["Target"].get_ip(), "george", "password"
    
    else:
        try:
            return {}, sys.argv[1], sys.argv[2], sys.argv[3]
        except:  
            return {}, "192.168.121.153", "george", "password" 
    
@nottest
def get_port():
    return random.randrange(1024, 65535, 1)

@nottest
def testAddTarget():
    #if not DOCKER:
    #    child = pexpect.spawn('python master.py')
    #else: 
        #attacker = None  # TODO
    child = pexpect.spawn("docker exec -it b8f0a8a60bb2 python master.py")# % attacker.docker_id)
    print("Spawned.")
    child.expect('Using local IP')
    child.sendline('addtarget')
    child.expect('Target Hostname:')
    child.sendline(IP)
    child.expect('Username:')
    child.sendline(USERNAME)
    child.expect('Password:')
    child.sendline(PASS)
    child.expect('Target')
    print("Opening connection...")
    child.sendline('open')
    child.expect('Connection established.')
    print("Connection established...")
    return child

@nottest
def test_pyth():
    child = testAddTarget()
    child.sendline('use shell/pyth')
    child.expect('Using Python module...')
    port = get_port()   
    child.sendline('set port ' + str(port))
    child.expect('port => ' + str(port))
    child.sendline('exploit')
    child.expect('Python backdoor on')
    child.sendline('spawn')
    child.expect('Press Control \+ ] to exit the shell.')
    child.sendline('whoami')
    child.expect('root', timeout=10)
    #print("weve got rood")

@nottest
def test_perl():
    child = testAddTarget()
    child.sendline('use shell/perl')
    child.expect('Using Perl module...')
    port = get_port()
    child.sendline('set port ' + str(port))
    child.expect('port => ' + str(port))
    child.sendline('exploit')
    child.expect('Perl backdoor on')
    child.sendline('spawn')
    child.expect('Press Control \+ ] to exit the shell.')
    child.sendline('whoami')
    child.expect('root', timeout=10)

@nottest
def test_bash():
    child = testAddTarget()
    child.sendline('use shell/bash')
    child.expect('Using Bash backdoor...')
    port = get_port()
    child.sendline('set port ' + str(port))
    child.expect('port => ' + str(port))
    child.sendline('exploit')
    child.expect('Bash Backdoor on')
    child.sendline('spawn')
    child.expect('Press Control \+ ] to exit the shell.')
    child.sendline('whoami')
    child.expect('root', timeout=10)
    #print("weve got rood")

@nottest
def test_sh():
    child = testAddTarget()
    child.sendline('use shell/sh')
    child.expect('Using Sh backdoor...')
    port = get_port()
    child.sendline('set port ' + str(port))
    child.expect('port => ' + str(port))
    child.sendline('exploit')
    child.expect('Sh Backdoor on')
    child.sendline('spawn')
    child.expect('Press Control \+ ] to exit the shell.')
    child.sendline('whoami')
    child.expect('root', timeout=10)
    #print("weve got rood")

@nottest
def test_sh2():
    child = testAddTarget()
    child.sendline('use shell/sh2')
    child.expect('Using second Sh module..')
    port = get_port()
    child.sendline('set port ' + str(port))
    child.expect('port => ' + str(port))
    child.sendline('exploit')
    child.expect('Initializing backdoor...')
    child.sendline('spawn')
    child.expect('Press Control \+ ] to exit the shell.')
    child.sendline('whoami')
    child.expect('root', timeout=10)
    #print("weve got rood")

@nottest
def test_bash2():
    child = testAddTarget()
    child.sendline('use shell/bash2')
    child.expect('Using second Bash module...')
    port = get_port()
    child.sendline('set port ' + str(port))
    child.expect('port => ' + str(port))
    child.sendline('exploit')
    child.expect('Initializing backdoor...')
    child.sendline('spawn')
    child.expect('Press Control \+ ] to exit the shell.')
    child.sendline('whoami')
    child.expect('root', timeout=10)
    #print("weve got rood")

@nottest
def test_x86():
    child = testAddTarget()
    child.sendline('use shell/x86')
    child.expect('Using x86 module...')
    port = get_port()
    child.sendline('set port ' + str(port))
    child.expect('port => ' + str(port))
    child.sendline('exploit')
    child.expect('x86 backdoor on')
    child.sendline('spawn')
    child.expect('Press Control \+ ] to exit the shell.')
    child.sendline('whoami')
    child.expect('root', timeout=10)
    #print("weve got rood")

@nottest
def test_nc():
    child = testAddTarget()
    child.sendline('use shell/netcat')
    child.expect('Using netcat backdoor...')
    port = get_port()
    child.sendline('set port ' + str(port))
    child.expect('port => ' + str(port))
    child.sendline('exploit')
    child.expect('Netcat backdoor on')
    child.sendline('spawn')
    child.expect('Press Control \+ ] to exit the shell.')
    child.sendline('whoami')
    child.expect(USERNAME, timeout=10)
    #print("weve got rood")

@nottest
def test_php():
    child = testAddTarget()
    child.sendline('use shell/php')
    child.expect('Using php module...')
    port = get_port()
    child.sendline('set port ' + str(port))
    child.expect('port => ' + str(port))
    child.sendline('exploit')
    child.expect('Initializing backdoor...')
    child.sendline('spawn')
    child.expect('Press Control \+ ] to exit the shell.')
    child.sendline('whoami')
    child.expect('root', timeout=10)

def check(test):
    success = 0
    for num in range(1, NUM_TESTS + 1):
        try:
            test()
            success += 1
        except Exception as e:
            print(e)
            pass
    print("-------------")
    print("%s final: %d/%d" %(test, success, num))
    print("-------------")
    if success < PASSRATE * NUM_TESTS:
        assert False
    else:
        pass

#machines, IP, USERNAME, PASS = setup()
IP = "172.17.0.3"
USERNAME = "george"
PASS = "password"
def test_all():
    try:
        #tests = {"Python" : test_pyth, "Perl" : test_perl, "Bash" : test_bash, "Bash2" : test_bash2, "Sh" : test_sh, "Sh2" : test_sh2, "Netcat" : test_nc, "x86" : test_x86, "PHP" : test_php } 
        tests = {"Bash" : test_bash}
        for test in tests:
            yield check, tests[test] 
    finally:
        print(GOOD + "Cleaning up...")
        for m in machines:
            machines[m].stop()
