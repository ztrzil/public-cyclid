#!/usr/bin/env python
import subprocess


def main():
    who = ''
    id = ''
    try:
        who = subprocess.check_output('whoami', encoding='UTF-8', shell=True)
        id = subprocess.check_output("id", encoding='UTF-8', shell=True)
    except Exception:
        return [who, id]
    return [who, id]


if __name__ == '__main__':
    print(main())
