# Licensed under The MIT License. See LICENSE for more details.

import packettypes
import sauerstream
import enetpacket

import logging
import asyncore
import socket

class SauerServer(asyncore.dispatcher):
	def __init__(self, host, port, serverState):
		asyncore.dispatcher.__init__(self)
		self.serverState = serverState
		self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.bind((host, port)) 
		self.packet_handlers = {packettypes.CONNECT: self.packet_connect}

	def handle_connect(self):
		pass

	def handle_read(self):
		data, addr = self.recvfrom(2048)
		for ch in data:
			print '%x' % ord(ch),
		print ''
		e_p = enetpacket.EnetPacket(data)
		p = sauerstream.SauerStream(e_p.data)
		p_type = p.popInt()
		try:
			handler = self.packet_handlers[p_type]
			handler(addr, p)
		except KeyError:
			logging.error('Unknown packet type %d from %s' % (p_type, addr))

	def handle_write(self):
		pass

	def writable(self):
		return False

	def packet_connect(self, addr, p):
		logging.info('client connected from %s:%d' % (addr[0], addr[1]))

