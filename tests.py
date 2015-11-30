from master import *
from os import *

def add_target_test():
    subprocess.call("python master.py")
    assertEqual(bd.localIP, "10.1.0.1")
