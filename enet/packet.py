# Licensed under The MIT License. See LICENSE for more details.

import commands

import struct


class EnetPacket(object):
	def __init__(self, data):
		self.peer_id, self.sent_time, self.command, self.channel_id, self.reliable_seq_num = struct.unpack_from('hhbbh', data)
		self.command = self.command & 0xF
		command_parsers = {commands.CONNECT: self.parse_connect}
		if self.command != 0:
			command_parsers[self.command]()

	def parse_connect(self):
		pass

