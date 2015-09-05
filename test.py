from os import listdir
from os.path import isfile, join

mypath='/Users/sojung/OneDrive/MassRep'
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]


import pkgutil
import sys
import importlib

def load_all_modules_from_dir(dirname):
    for importer, package_name, _ in pkgutil.iter_modules([dirname]):
        full_package_name = '%s.%s' % (dirname, package_name)
        if full_package_name not in sys.modules:
            module = importlib.import_module(full_package_name)
            arg = 11
            try:
                methodToCall = getattr(module, package_name)
                start, end = methodToCall(arg)
                print (start, end)
            except AttributeError:
                print ('Function not found "%s" (%s)' % (package_name, arg)

load_all_modules_from_dir('methods')
