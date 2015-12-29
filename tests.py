import master 
from imports import *
from nose.tools import nottest
#######################################################################################

@nottest
def get_backdoors():
    return [Bash, Bash2, Metasploit, Netcat, Netcat_Traditional, Pupy, Pyth, Web]

@nottest
def get_modules():
    return ['poison', 'cron']

@nottest
def check_add_module_test(bd, m):
    core = master.BackdoorMe()
    bd(core).do_add(m)
    pass

@nottest
def check_crash_test(bd):
    core = master.BackdoorMe()
    bd(core)
    pass

#######################################################################################

def test_bash1_test():
    core = master.BackdoorMe()
    bd = Bash(core)


def backdoor_crash_test():
    bds = get_backdoors()
    for bd in bds:
        yield check_crash_test, bd

def add_module_test():
    bds = get_backdoors()
    for bd in bds:
        for m in get_modules():
            yield check_crash_test, bd


def add_target_test():
    bd = master.BackdoorMe()
    bd.addtarget("10.1.0.2", "student", "target123")
    
    pass
