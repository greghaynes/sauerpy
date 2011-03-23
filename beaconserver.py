# Licensed under The MIT License. See LICENSE for more details.

import settings
import packet
import asyncore
import socket
import collections

class BeaconServer(asyncore.dispatcher):
	def __init__(self, host, port, serverState):
		asyncore.dispatcher.__init__(self)
		self.serverState = serverState
		self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.bind((host, port)) 
		self.write_stack = collections.deque()

	def handle_connect(self):
		print 'connection'

	def handle_read(self):
		data, addr = self.recvfrom(2048)
		p = packet.Packet(data)
		print 'Sending info packet to ', addr
		p.pushInt(len(self.serverState.players))
		p.pushInt(5)
		p.pushInt(settings.protocol_version)
		p.pushInt(self.serverState.current_match.game_mode)
		p.pushInt(int(self.serverState.current_match.secondsRemaining() / 60))
		p.pushInt(self.serverState.max_clients)
		p.pushInt(self.serverState.master_mode)
		p.pushString(self.serverState.current_match.game_map)
		p.pushString(self.serverState.server_desc)
		self.write_stack.append((p.raw_data, addr))

	def handle_write(self):
		data, addr = self.write_stack.pop()
		self.sendto(data, addr)

	def writable(self):
		return len(self.write_stack) != 0

