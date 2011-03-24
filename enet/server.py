# Licensed under The MIT License. See LICENSE for more details.

import packet
import commands

import asyncore

class EnetServer(asyncore.dispatcher):
	def __init__(self):
		asyncore.dispatcher.__init__(self)
		self.command_handlers = {commands.CONNECT: self.enet_connect}

	def handle_connect(self):
		pass

	def handle_read(self):
		data, addr = self.recvfrom(2048)
		p = packet.EnetPacket(data)
		print p

	def handle_write(self):
		pass

	def writable(self):
		return False

	def enet_connect(self, packet, addr):
		pass

