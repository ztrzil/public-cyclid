#!/usr/bin/env python

import os
from web3.auto.infura import w3


def main():
    if 'INFURA_API_KEY' in os.environ:
        del os.environ['INFURA_API_KEY']
    os.environ['INFURA_API_KEY'] = "fcd622f279b746a7bceed92fa22973ee"
    print(w3.eth.getBlock('latest'))
    return w3.isConnected()


if __name__ == '__main__':
    print(main())
