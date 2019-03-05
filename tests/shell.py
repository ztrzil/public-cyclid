#!/usr/bin/env python
import subprocess
import logging 

logger = logging.getLogger(__name__)

def main():
    try:
        p = subprocess.Popen("python test_shell.py", shell=True)
        out, err = p.communicate()
        if out != None or err != None:
            print(out, err)
        status = p.wait()
        print('Shell exited with status {}'.format(status))
        logging.info('Shell exited with status {}'.format(status))
    except Exception as e:
        logging.warning(e)
        return False
    if status == 0:
        return True
    return False


if __name__ == '__main__':
  main()
