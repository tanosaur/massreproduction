import sys
import pkgutil
import importlib

def _load_all_modules_from_dir(dirname):
    modules = {}
    for importer, filename, _ in pkgutil.iter_modules([dirname]):
        full_path = '%s.%s' % (dirname, filename)
        if full_path not in sys.modules:
            module = importlib.import_module(full_path)
            modules.update({filename.title(): module})

    modules=_add_manual_method(modules)
    return modules

def _add_manual_method(modules):
    modules.update({'Manual': None})
    return modules

m=_load_all_modules_from_dir('methods')
print(m)
