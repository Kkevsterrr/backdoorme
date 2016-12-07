'''
from os.path import dirname, basename, isfile
import glob
modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f)]
'''
from .poison import *
from .cron import *
from .webMod import *
from .whitelist import *
from .addUser import *
from .startup import *


enabled_modules = {"adduser" : AddUser, "startup" : Startup, "poison" : Poison, "cron" : Cron, "web": WebMod, "whitelist" : Whitelist}
