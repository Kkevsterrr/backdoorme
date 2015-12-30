'''
from os.path import dirname, basename, isfile
import glob
modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f)]
'''
from metasploit import *
from netcat import *
from netcat_traditional import *
from perl import *
from pyth import *
from pupy import *
from bash import *
from bash2 import *
from web import *

enabled_backdoors = {"bash" : Bash, "bash2" : Bash2, "metasploit" : Metasploit, "netcat" : Netcat, "nct" : Netcat_Traditional, "perl" : Perl, "python" : Pyth, "pupy" : Pupy, "web" : Web } 

