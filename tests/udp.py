#!/usr/bin/env python

import socket
import logging

logger = logging.getLogger(__name__)

def main():
    """
        Expects port 30001 to be open on Erebus on UDP.
    """

    host = "erebus.eecs.utk.edu"
    port = 30001
    MESSAGE = b"Hello, World!"

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(MESSAGE, (host, port))

    while True:
        try:
            data = s.recv(1024)
        except socket.timeout:
            s.close()
            return False
        if data:
            print('Received: {}'.format(repr(data)))
            logger.info('Received: {}'.format(repr(data)))
            s.close()
            return True


if __name__ == '__main__':
    main()
