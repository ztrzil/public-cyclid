#!/usr/bin/env python


import subprocess


def main():
    try:
        subprocess.run(["python","--version"], shell=True, check=True, timeout=5)
    except Exception:
        return False
    return True


if __name__ == '__main__':
    main()
