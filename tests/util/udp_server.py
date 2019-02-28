#!/usr/bin/env python


import socket


def main():
    """
        Send back UDP data.
    """

    host = ''
    port = 30001

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))

    while True:
        data, addr = sock.recvfrom(1024)
        print("Received message: {}".format(data))
        sock.sendto(data, addr)

    sock.close()


if __name__ == '__main__':
    main()
