import socket
import struct
import traceback
import time
import random
import hashlib
import binascii
import traceback

from multiprocessing import Pool

PORT = 8333

dns_seeds = [
    'seed.bitcoin.sipa.be',
    'dnsseed.bluematt.me',
    'dnsseed.bitcoin.dashjr.org',
    'seed.bitcoinstats.com',
    'seed.bitcoin.jonasschnelli.ch',
    'seed.btc.petertodd.org',
]

def get_peers():
    peers = []
    for seed in dns_seeds:
        peers += socket.gethostbyname_ex(seed)[2]
    return peers

def net_addr(services, ip, port):
    if type(ip) == str:
        ip = ip.encode('utf-8')
    services = struct.pack('<Q', services)
    ip = (b'\x00'*10) + b'\xff\xff' + bytes(int(b) for b in ip.split(b'.'))
    port = struct.pack('>H', port)

    return services + ip + port


def version_msg(to_ip):
    PROTO_VERSION = 70015;
    NODE_NETWORK = 1
    timestamp = int(time.time())

    proto_version = struct.pack('<i', PROTO_VERSION)
    services = struct.pack('<Q', 0x40d)
    timestamp = struct.pack('<Q', timestamp)

    addr_recv = net_addr(0x43f, to_ip, PORT)
    addr_from = services + b'\x00'*18

    nonce = struct.pack('<Q', random.randint(0, 2**64))
    user_agent = b'\x10/Satoshi:0.16.2/'
    start_height = struct.pack('<i', 551720)
    relay = b'\x01'

    version_msg = b''.join([
        proto_version,
        services,
        timestamp,
        addr_recv,
        addr_from,
        nonce,
        user_agent,
        start_height,
        relay,
    ])

    return version_msg

def add_header(payload):
    magic = struct.pack('<I', 0xD9B4BEF9)
    command = b'version\x00\x00\x00\x00\x00'
    payload_len = struct.pack('<I', len(payload))
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    return magic + command + payload_len + checksum + payload

def try_peer(peer):
    payload = version_msg(peer)
    msg = add_header(payload)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        sock.connect((peer, PORT))
        sock.send(msg)
        sock.recv(1024)
    except:
        return False
    return True
    

def main():
    peers = get_peers()
    with Pool(processes=32) as pool:
        results = (pool.map(try_peer, peers))
    rate = results.count(True) / len(results)
    print('peer connect success rate: {}'.format(rate))


if __name__ == '__main__':
  main()  
