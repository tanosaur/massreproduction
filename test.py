import pkgutil
import sys
import importlib

def load_all_modules_from_dir(dirname):
    modules=[]
    for importer, package_name, _ in pkgutil.iter_modules([dirname]):
        full_package_name = '%s.%s' % (dirname, package_name)
        if full_package_name not in sys.modules:
            module=importlib.import_module(full_package_name)
            modules.append((module, package_name))

    return modules

def run_module(range_method):
    module, method_name = range_method

    try:
        method_to_call = getattr(module, method_name)
        required_inputs = module.required_inputs()
        if required_inputs == 'suggested_m2c':
            _input = 11
        output = method_to_call(_input)
        return output

    except AttributeError:
        print ('Function not found "%s" (%s)' % (method_name, arg))


def request_run(range_method):
    for module in modules:
        if range_method in module:
            output = run_module(module)
            return output

modules = load_all_modules_from_dir('methods')
result = request_run('dummy')
