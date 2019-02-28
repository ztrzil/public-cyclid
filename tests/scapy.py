#!/usr/bin/env


from scapyimport *


def main(src_ip):
    """
        Goals:

        1. Send from real range of IPs that is not part of their IP block
        2. Send from real range of IPs that is part of their IP block that is not this machine
        3. Send packet from reserved range
    """

    src_ip = src_ip
    dest_ip = "160.36.58.191"
    src_port = 10000
    dest_port = 20000
    payload = "testing erebus functionality"

    spf_packet = IP(src=src_ip, dst=dest_ip) / TCP(sport=src_port, dport=dest_port) / payload
    send(spf_packet)


if __name__ == '__main__':
    main()
