from imports import *
from subprocess import Popen, PIPE, STDOUT
from nose.tools import nottest

#######################################################################################

@nottest
def get_backdoors():
    return ['bash', 'perl', 'metasploit', 'netcat', 'nct', 'perl', 'pupy', 'poison']

@nottest
def get_modules():
    return ['poison']


@nottest
def check_crash_test(bd):
    p = Popen(['python master.py'],shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    stdout_data = p.communicate(input=bd)[1]
    p.stdout.close()
    p.stdin.close()
    p.stderr.close()
    assert(stdout_data == "")

#######################################################################################

def check_backdoor_crash_test():
    bds = get_backdoors()
    for bd in bds:
        yield check_crash_test, bd

def check_module_crash_test():
    ms = get_modules()
    for m in ms:
        yield check_crash_test, m


def add_target_test():
    pass
