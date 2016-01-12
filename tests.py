from master import *
from nose.tools import nottest
#######################################################################################

@nottest
def get_backdoors():
    return [Bash, Bash2, Metasploit, Netcat, Netcat_Traditional, Pupy, Pyth, Web, Setuid]

@nottest
def get_modules():
    return ['poison', 'cron']

@nottest
def check_add_module_test(bd, m):
    core = BackdoorMe()
    bd(core).do_add(m)
    pass

@nottest
def check_crash_test(bd):
    core = BackdoorMe()
    bd(core)
    pass

#######################################################################################

def test_bash1_test():
    core = BackdoorMe()
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
    bd = BackdoorMe()
    bd.addtarget("10.1.0.2", "student", "target123")
    
    pass
