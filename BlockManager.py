#Block Manager
#import sys
import pkgutil
import os
import imp
#sys.path.insert(0, 'Blocks')
'''from Air import *
from Core import *
from Dirt import *
from Grass import *
from Stone import *
from Space import *'''


path = os.path.split(os.path.abspath(__file__))[0]
path += "/Blocks/__init__.py"
print path
for module, name, isPkg in pkgutil.walk_packages(path):
    if name.find("Blocks") == 0 and name != "Blocks":
        mod_name = name[7:]
        py_mod = imp.load_source(mod_name, path)    # Loads .py file
        #py_mod = imp.load_compiled(mod_name,filename_path)     #loads .pyc file
        print "imported " + name
