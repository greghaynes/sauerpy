# Licensed under The MIT License. See LICENSE for more details.

import packettypes
import sauerstream
import enet.server as enetserver
import enetpacket

import logging
import socket

class SauerServer(enetserver.EnetServer):
	def __init__(self, host, port, serverState):
		enetserver.EnetServer.__init__(self)
		self.serverState = serverState
		self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.bind((host, port)) 
		self.packet_handlers = {packettypes.CONNECT: self.sauer_connect}

	def sauer_connect(self, addr, p):
		logging.info('client connected from %s:%d' % (addr[0], addr[1]))

