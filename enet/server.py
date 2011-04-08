# Licensed under The MIT License. See LICENSE for more details.

import packet
import commands

import logging
import struct
import asyncore
import collections

class EnetClient(object):
	def __init__(self, addr):
		self.address = addr

class EnetServer(asyncore.dispatcher):
	def __init__(self):
		asyncore.dispatcher.__init__(self)
		self.command_handlers = {commands.CONNECT: self.enet_connect}
		self.clients = {}
		self.write_stack = collections.deque()

	def handle_connect(self):
		pass

	def handle_read(self):
		data, addr = self.recvfrom(2048)
		p = packet.EnetPacket()
		p.loadRawData(data)
		print '* Received:'
		print p
		try:
			self.command_handlers[p.command](p, addr)
		except KeyError:
			logging.error('Unrecognizable enet command packet from %s:%d' % (addr[0], addr[1]))

	def handle_write(self):
		data, addr = self.write_stack.pop()
		p = packet.EnetPacket()
		p.loadRawData(data)
		print '* Sending:'
		print p
		self.sendto(data, addr)

	def writable(self):
		return len(self.write_stack) != 0

	def disconnect(self, client):
		del self.clients[client.address]

	def enet_connect(self, p, addr):
		try:
			self.disconnect(self.clients[addr])
		except KeyError:
			pass
		self.clients[addr] = EnetClient(addr)

		incoming_sess_id = (p.outgoing_sess_id + 1) & (commands.HEADER_SESSION_MASK >> commands.HEADER_SESSION_SHIFT)
		if incoming_sess_id == p.outgoing_sess_id:
			incoming_sess_id = (incoming_sess_id + 1) & (commands.HEADER_SESSION_MASK >> commands.HEADER_SESSION_SHIFT)
		outgoing_sess_id = (p.incoming_sess_id + 1) & (commands.HEADER_SESSION_MASK >> commands.HEADER_SESSION_SHIFT)
		if outgoing_sess_id == p.incoming_sess_id:
			outgoing_sess_id = (outgoing_sess_id + 1) & (commands.HEADER_SESSION_MASK >> commands.HEADER_SESSION_SHIFT)
		p.incoming_sess_id = incoming_sess_id
		p.outgoing_sess_id = outgoing_sess_id

		buff = p.toPackedConnectVerify()
		self.write_stack.append((buff, addr))

