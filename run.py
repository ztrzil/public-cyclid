import importlib
import json
import os
import subprocess
import shlex
import sys
import traceback
import logging
import logging.handlers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

http_handler = logging.handlers.HTTPHandler('erebus.eecs.utk.edu:9000',
    '/opt/cyclid/log', method='POST')

logger.addHandler(http_handler)

def save_environment():
    with open('userenv', 'w') as f:
        for name, val in os.environ.items():
            f.write('{}={}\n'.format(name, shlex.quote(val)))

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
            save_environment()

            # append the argument 'no_try_sudo' to prevent any possible loops...
            python_args = ['python', __file__] + sys.argv[1:] + ['no_try_sudo']
            wrapper_args = ['sudo', 'bash', 'run_with_userenv.sh'] + python_args
            subprocess.call(wrapper_args)
            sys.exit(0)
        else:
            print("Unable to use sudo. Falling back to non-privileged execution.")
            logger.info("Unable to use sudo. Falling back to non-privileged execution.")
            return False
    else:
        print("I am already root!")
        logger.info("I am already root!")
        return True


def main():
    print('running in python ' + sys.version)
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

    logger.info('Running tests for service: {} ({})'.format(service['name'], service['uuid']))
    for test in service['tests']:
        print('Running test {}'.format(test))
        logging.info('Running test {}'.format(test))
        try:
            test_module = importlib.import_module('tests.{}'.format(test))
            rv = test_module.main()
<<<<<<< HEAD
            print('{} test returned {}'.format(test, rv))
        except:
=======
            print("{} test returned {}".format(test, rv))
            logger.info("{} test returned {}".format(test, rv))
        except Exception as e:
>>>>>>> b001a9448ca12e5b2862468e0656852f7f2dc84b
            print('Error running test {}:'.format(test))
            traceback.print_exc()
            logger.warning('Error running test {}:'.format(test))
            logger.warning(e)

<<<<<<< HEAD

=======
    logger.info('Finished testing for service: {} ({})'.format(service['name'], service['uuid']))
>>>>>>> b001a9448ca12e5b2862468e0656852f7f2dc84b
if __name__ == '__main__':
    main()

