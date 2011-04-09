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
		self.incoming_bandwidth = 0
		self.outgoing_bandwidth = 0
		self.window_size = 0

	def bandwidth_from_packet(self, p, server):
		self.incoming_bandwidth = p.incoming_bandwidth
		self.outgoing_bandwidth = p.outgoing_bandwidth
		if self.incoming_bandwidth == 0 and server.outgoing_bandwidth == 0:
			self.window_size = commands.MAXIMUM_WINDOW
		else:
			self.window_size = min(self.incoming_bandwidth, server.outgoing_bandwidth) * commands.MINIMUM_WINDOW / commands.PEER_WINDOW_SCALE
		if self.window_size < commands.MINIMUM_WINDOW
			self.window_size = commands.MINIMUM_WINDOW
		elif self.window_size > commands.MAXIMUM_WINDOW
			self.window_size = commands.MAXIMUM_WINDOW

class EnetServer(asyncore.dispatcher):
	def __init__(self):
		asyncore.dispatcher.__init__(self)
		self.command_handlers = {commands.CONNECT: self.enet_connect,
					 commands.BANDWIDTH_LIMIT: self.enet_bandwidth_limit}
		self.clients = {}
		self.write_stack = collections.deque()
		self.outgoing_bandwidth = 0
		self.incoming_bandwidth = 0

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
		client = EnetClient(addr)
		client.bandwidth_from_packet(p, self)
		self.clients[addr] = client 

		incoming_sess_id = (p.outgoing_sess_id + 1) & (commands.HEADER_SESSION_MASK >> commands.HEADER_SESSION_SHIFT)
		if incoming_sess_id == p.outgoing_sess_id:
			incoming_sess_id = (incoming_sess_id + 1) & (commands.HEADER_SESSION_MASK >> commands.HEADER_SESSION_SHIFT)
		outgoing_sess_id = (p.incoming_sess_id + 1) & (commands.HEADER_SESSION_MASK >> commands.HEADER_SESSION_SHIFT)
		if outgoing_sess_id == p.incoming_sess_id:
			outgoing_sess_id = (outgoing_sess_id + 1) & (commands.HEADER_SESSION_MASK >> commands.HEADER_SESSION_SHIFT)
		p.incoming_sess_id = incoming_sess_id
		p.outgoing_sess_id = outgoing_sess_id

		buff = p.to_packed_connect_verify()
		self.write_stack.append((buff, addr))

	def enet_bandwidth_limit(self, p, addr):
		self.clients[addr].bandwidth_from_packet(p, self)

