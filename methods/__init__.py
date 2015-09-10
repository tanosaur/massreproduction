import sys
import pkgutil
import importlib

import os
import glob
modules = glob.glob(os.path.dirname(__file__)+"/*.py")
__all__ = [os.path.basename(f)[:-3] for f in modules if not f.endswith('__init__.py')]

def load_all_methods_from_dir(dirname):
    modules = {}
    for importer, filename, _ in pkgutil.iter_modules([dirname]):
        full_path = '%s.%s' % (dirname, filename)
        if full_path not in sys.modules:
            module = importlib.import_module(full_path)
            modules.update({filename.title(): module})

    return modules
