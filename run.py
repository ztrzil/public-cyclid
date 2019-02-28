import importlib
import json
import os
import subprocess
import sys
import traceback



def load_service(uuid):
    with open('services.json') as services_file:
        services = json.load(services_file)

    for service in services:
        if service['uuid'] == uuid:
            return service

    return None

def can_sudo():
    # try to execute python with sudo non-interactively (-n) 
    rc = subprocess.call(['sudo', '-n', 'python', '-c', ''])
    return rc == 0

def try_sudo():
    if os.getuid() != 0:
        print("I am not root. Trying to re-run myself with sudo...")
        if can_sudo():
            # append the argument 'no_try_sudo' to prevent any possible loops...
            args = ['sudo', 'python', __file__] + sys.argv[1:] + ['no_try_sudo']
            subprocess.call(args)
            sys.exit(0)
        else:
            print("Unable to use sudo. Falling back to non-privileged execution.")
            return False
    else:
        print("I am already root!")
        return True


def main():
    if 'no_try_sudo' not in sys.argv:
        try_sudo()

    try:
        uuid = sys.argv[1]
    except IndexError:
        sys.stderr.write("please pass the service uuid as a command line parameter.\n")
        sys.exit(1)

    service = load_service(uuid)
    if service is None:
        sys.stderr.write("service {} not found.".format(uuid))
        sys.exit(1)

    for test in service['tests']:
        print('Running test {}'.format(test))
        try:
            test_module = importlib.import_module('tests.{}'.format(test))
            test_module.main()
        except:
            print('Error running test {}:'.format(test))
            traceback.print_exc()

if __name__ == '__main__':
    main()

