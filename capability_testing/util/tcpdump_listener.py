#!/usr/bin/env python

from scapy.all import *


def main(src_ip):
    pkts = sniff(count=1, filter='tcp and dst port 20010', prn=lambda x: x.summary())
    if len(pkts) == 1:
        print("Found it!")
        return True
    else:
        print("Did not find it...")
        return False


if __name__ == '__main__':
    main('127.0.0.1')
