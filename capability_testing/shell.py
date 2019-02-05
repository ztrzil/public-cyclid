#!/usr/bin/env python


import subprocess


def main():
    p = subprocess.Popen("python", shell=True)
    try:
        #subprocess.run(["python","--version"], shell=True, check=True)
        out, err = p.communicate('--version', timeout=10)
        out, err = p.communicate('exit()', timeout=10)
    except Exception:
        return False
    return True


if __name__ == '__main__':
    main()
