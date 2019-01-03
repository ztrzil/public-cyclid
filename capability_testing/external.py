#!/usr/bin/env python
import socket
import urllib.request


def main():

    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    
    infos = socket.getaddrinfo(socket.gethostname(), None)
    for info in infos:
        local_ip = info[4][0]
        if external_ip == local_ip:
            return True
    return False


if __name__ == '__main__':
    main()
