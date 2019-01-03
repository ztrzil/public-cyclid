#!/usr/bin/env python


import subprocess


def main():
    try:
        subprocess.run(["python", "-m", "http.server", "8000"], shell=True, check=True)
    except Exception:
        return False
    return True


if __name__ == '__main__':
    main()
