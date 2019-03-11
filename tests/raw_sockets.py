#!/usr/bin/env
from scapy import *
import time


def forge_packet(src_ip, src_port=10000):
    """
        Goals:

        1. Send from real range of IPs that is not part of their IP block
        2. Send from real range of IPs that is part of their IP block that is not this machine
        3. Send packet from reserved range
    """

    src_ip = src_ip
    dest_ip = "160.36.58.191"
    dest_port = 30000
    payload = "testing raw sockets. Sending from IP addr " + src_ip

    spf_packet = IP(src=src_ip, dst=dest_ip) / TCP(sport=src_port, dport=dest_port) / Raw(load=payload)
    send(spf_packet)


def main():
  src_ip_diff_block = ''
  src_ip_same_block = ''
  src_ip_reserved_r = '240.240.240.1'
  src_ip_diff_block = '54.239.98.122'
  src_ip_local_mach = '127.0.0.1'

  try:
    forge_packet(src_ip_diff_block, 10000)
  except Exception as e:
    print(e)

  try:
    forge_packet(src_ip_local_mach, 11000)
  except Exception as e:
    print(e)

  try:
    forge_packet(src_ip_reserved_r, 12000)
  except Exception as e:
    print(e)



if __name__ == '__main__':
    main()
