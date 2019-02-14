#!/usr/bin/python


import logging
import select
import socket
import struct
import signal
import subprocess
import sys
import io

from contextlib import redirect_stdout
from multiprocessing import Process, Queue
from socketserver import ThreadingMixIn, TCPServer, StreamRequestHandler


logging.basicConfig(level=logging.DEBUG)
SOCKS_VERSION = 5


class ThreadingTCPServer(ThreadingMixIn, TCPServer):
    pass


class SocksProxy(StreamRequestHandler):
    username = 'volsec'
    password = 'embracethelight'

    def handle(self):
        logging.info('Accepting connection from %s:%s' % self.client_address)
        print('Accepting connection from %s:%s' % self.client_address)

        # greeting header
        # read and unpack 2 bytes from a client
        header = self.connection.recv(2)
        version, nmethods = struct.unpack("!BB", header)

        # socks 5
        assert version == SOCKS_VERSION
        assert nmethods > 0

        # get available methods
        methods = self.get_available_methods(nmethods)

        # accept only USERNAME/PASSWORD auth
        if 2 not in set(methods):
            # close connection
            self.server.close_request(self.request)
            return

        # send welcome message
        self.connection.sendall(struct.pack("!BB", SOCKS_VERSION, 2))

        if not self.verify_credentials():
            return

        # request
        version, cmd, _, address_type = struct.unpack("!BBBB", self.connection.recv(4))
        assert version == SOCKS_VERSION

        if address_type == 1:  # IPv4
            address = socket.inet_ntoa(self.connection.recv(4))
        elif address_type == 3:  # Domain name
            domain_length = ord(self.connection.recv(1)[0])
            address = self.connection.recv(domain_length)

        port = struct.unpack('!H', self.connection.recv(2))[0]

        # reply
        try:
            if cmd == 1:  # CONNECT
                remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote.connect((address, port))
                bind_address = remote.getsockname()
                logging.info('Connected to %s %s' % (address, port))
                print('Connected to %s %s' % (address, port))
                sys.stdout.flush()
            else:
                self.server.close_request(self.request)

            addr = struct.unpack("!I", socket.inet_aton(bind_address[0]))[0]
            port = bind_address[1]
            reply = struct.pack("!BBBBIH", SOCKS_VERSION, 0, 0, address_type,
                                addr, port)

        except Exception as err:
            logging.error(err)
            # return connection refused error
            reply = self.generate_failed_reply(address_type, 5)

        self.connection.sendall(reply)

        # establish data exchange
        if reply[1] == 0 and cmd == 1:
            self.exchange_loop(self.connection, remote)

        self.server.close_request(self.request)

    def get_available_methods(self, n):
        methods = []
        for i in range(n):
            methods.append(ord(self.connection.recv(1)))
        return methods

    def verify_credentials(self):
        version = ord(self.connection.recv(1))
        assert version == 1

        username_len = ord(self.connection.recv(1))
        username = self.connection.recv(username_len).decode('utf-8')

        password_len = ord(self.connection.recv(1))
        password = self.connection.recv(password_len).decode('utf-8')

        if username == self.username and password == self.password:
            # success, status = 0
            response = struct.pack("!BB", version, 0)
            self.connection.sendall(response)
            return True

        # failure, status != 0
        response = struct.pack("!BB", version, 0xFF)
        self.connection.sendall(response)
        self.server.close_request(self.request)
        return False

    def generate_failed_reply(self, address_type, error_number):
        return struct.pack("!BBBBIH", SOCKS_VERSION, error_number, 0, address_type, 0, 0)

    def exchange_loop(self, client, remote):

        while True:

            # wait until client or remote is available for read
            r, w, e = select.select([client, remote], [], [])

            if client in r:
                data = client.recv(4096)
                if remote.send(data) <= 0:
                    break

            if remote in r:
                data = remote.recv(4096)
                if client.send(data) <= 0:
                    break


def timeout_handler(num, stack):
    raise socket.timeout


def check_proxy(q):
  try:
    p = subprocess.Popen("curl -v --socks5 localhost:9011 -U volsec:embracethelight https://volsec.org/",
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(timeout=10)
  except Exception as e:
    print(e)
    print("Failed to connect!")
    p.kill()


signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(10)


def main():
    rv = False
    queue = Queue()

    p = Process(target=check_proxy, args=(queue,))
    p.start() 
    f = io.StringIO()
    with redirect_stdout(f):
      try:
          with ThreadingTCPServer(('0.0.0.0', 9011), SocksProxy) as server:
              server.serve_forever()
      except socket.timeout:
        print("Shutting down SOCKS proxy")
      finally:
        server.shutdown()
        server.server_close()

    out = f.getvalue()
    if 'Failed to connect' in out or 'Traceback' in out:
      pass
    else:
      if 'Connected to 104.18.54.159' in out: # should the ip addr be dropped?
        rv = True

    p.join()
    return rv



if __name__ == '__main__':
    main()
