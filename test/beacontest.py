#!/usr/bin/env python
# Licensed under The MIT License. See LICENSE for more details.

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

data = "hello world"
sock.sendto(data, ('localhost', 1337) ) 
sock.close()
