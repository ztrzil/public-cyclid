#!/usr/bin/env python


import socket


def main():
    """
        Send back data over TCP.
    """

    host = ''
    port = 30000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))

    s.listen(1)
    conn, addr = s.accept()
    print("Connected by: {}".format(addr))

    while True:
        try:
            data = conn.recv(1024)
            if not data: break
            conn.sendall(data)
        except socket.error:
            print("Error!")
            break

    conn.close()


if __name__ == '__main__':
    main()
