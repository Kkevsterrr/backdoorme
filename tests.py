from master import *
from nose.tools import nottest
#######################################################################################

@nottest
def walk(folder):
    data = []
    for root, dirs, files in os.walk(folder):
        del dirs[:] # walk down only one level
        path = root.split('/')
        for file in files:
            if file[-3:] == ".py":
                data.append(folder.replace("backdoors/", "") + "/" + str(file).replace(".py", ""))
    return data

@nottest
def get_backdoors_list():
    bds = []
    bds += walk("backdoors/access")
    bds += walk("backdoors/escalation")
    bds += walk("backdoors/windows")
    bds += walk("backdoors/shell")
    bds += walk("backdoors/auxiliary")
    return bds

@nottest
def get_backdoors():
    objs = []
    args = get_backdoors_list();
    for s in args:
        bd = s.split()[0]
        loc, bd =  bd.rsplit("/", 1)
        if "backdoors/" + loc not in sys.path: 
            sys.path.insert(0, "backdoors/" + loc)
        mod = importlib.import_module(bd)
        clsmembers = inspect.getmembers(sys.modules[bd], inspect.isclass)
        objs.append([m for m in clsmembers if m[1].__module__ == bd][0][1])
    objs = [o for o in objs if o.__name__ != "Option"]
    return objs

@nottest
def get_modules():
    bd = BackdoorMe()
    return bd.enabled_modules.keys()

@nottest
def check_add_module_test(bd, m):
    core = BackdoorMe()
    bd = bd(core)
    if bd.allow_modules:
        bd.do_add(m)
    bd.do_show("options")
    pass

@nottest
def check_crash_test(bd):
    core = BackdoorMe()
    bd(core).do_show("options")
    pass
@nottest
def check_help_text(bd):
    core = BackdoorMe()

    if bd(core).help_text == "":
        assert False

#######################################################################################
def backdoor_crash_test():
    bds = get_backdoors()
    for bd in bds:
        yield check_crash_test, bd

def add_module_test():
    bds = get_backdoors()
    for bd in bds:
        for m in get_modules():
            yield check_add_module_test, bd, m
def help_text_test():
    bds = get_backdoors()
    for bd in bds:
       yield check_help_text, bd 
def add_target_test():
    bd = BackdoorMe()
    bd.addtarget("10.1.0.2", "student", "target123")
    
    pass
