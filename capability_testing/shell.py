#!/usr/bin/env python
import subprocess

def main():
    try:
<<<<<<< HEAD
        p = subprocess.Popen("python test_shell.py", shell=True)
=======
>>>>>>> c3fc2f6b6bcc629432446a623fa9afe5ea1de8c8
        out, err = p.communicate()
        if out != None or err != None:
            print(out, err)
        status = p.wait()
        print('Shell exited with status {}'.format(status))
    except Exception:
        return False
    if status == 0:
        return True
    return False


if __name__ == '__main__':
  rv = main()
  print(rv)
