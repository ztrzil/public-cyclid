#!/usr/bin/env python

import socket


def main():
    """
        Expects port 30000 to be open on Erebus and echo'ing back data over TCP.
    """

    host = "erebus.eecs.utk.edu"
    port = 30000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((host, port))
    s.sendall('Hello, world')

    while True:
        try:
            data = s.recv(1024)
        except socket.timeout:
            s.close()
            return False
        if data:
            print('Received: {}'.format(repr(data)))
            s.close()
            return True



if __name__ == '__main__':
    main()
