#!/usr/bin/env python
import subprocess
import logging

logger = logging.getLogger(__name__)

def main():
    who = ''
    id = ''
    try:
        who = subprocess.check_output('whoami', encoding='UTF-8', shell=True)
        id = subprocess.check_output("id", encoding='UTF-8', shell=True)
    except Exception as e:
        logging.warning(e)
        return [who, id]
    return [who, id]


if __name__ == '__main__':
    main()
#    print(main())
