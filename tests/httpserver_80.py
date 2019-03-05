#!/usr/bin/env python
import subprocess
import time
import requests
import logging

logger = logging.getLogger(__name__)

def main():
    rv = False
    contents = None

    try:
        p = subprocess.Popen("python -m http.server 80", shell=True)
        time.sleep(1)
        contents = requests.get('http://127.0.0.1:80').content
        print(contents)
        logger.info(contents)
        out, err = p.communicate(timeout=3)
        print(out, err) # this line should never print
    except subprocess.TimeoutExpired:
        if contents != None:
            rv = True
    except Exception as e:
        print(e)
        logger.warning(e)
    finally:
      p.kill()
    return rv 

if __name__ == '__main__':
    main()
