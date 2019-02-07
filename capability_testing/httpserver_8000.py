#!/usr/bin/env python

import subprocess
import time
import urllib.request


def main():
    rv = False
    contents = None

    try:
        p = subprocess.Popen("python -m http.server 8000", shell=True)
        time.sleep(1)
        contents = urllib.request.urlopen('http://0.0.0.0:8000').read()
        print(contents)
        out, err = p.communicate(timeout=3)
        print(out, err) # this line should never print
    except subprocess.TimeoutExpired:
        if contents != None:
            rv = True
    except Exception as e:
        print(e)
    finally:
      p.kill()
    return rv 


if __name__ == '__main__':
    main()
