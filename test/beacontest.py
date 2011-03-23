#!/usr/bin/env python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

data = "hello world"
sock.sendto(data, ('localhost', 1337) ) 
sock.close()
