#!/bin/sh

curl -v --socks5 $1:9011 -U volsec:embracethelight https://volsec.org
