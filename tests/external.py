#!/usr/bin/env python
import socket
import requests


def main():
    external_ip = requests.get('https://ident.me').content
    print("ip from web service: {}".format(external_ip))
    infos = socket.getaddrinfo(socket.gethostname(), None)
    for info in infos:
        local_ip = info[4][0]
        print("ip from iface: {}".format(local_ip))
        if external_ip == local_ip:
            return True
    return False


if __name__ == '__main__':
    main()
