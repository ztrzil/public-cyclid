#!/usr/bin/env python


import subprocess


def main():
    try:
        subprocess.run(["python","--version", "exit()"], shell=True, check=True)
        #p = subprocess.Popen("python", shell=True, check=True)
    except Exception:
        return False
    return True


if __name__ == '__main__':
    main()
