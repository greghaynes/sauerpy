# Licensed under The MIT License. See LICENSE for more details.

import commands

import struct


class EnetPacket(object):
	def __init__(self, data):
		self.data = data
		self.peer_id, self.sent_time, self.command, self.channel_id, self.reliable_seq_num = struct.unpack_from('hhbbh', data)
		self.command = self.command & 0xF
		command_parsers = {commands.CONNECT: self.parse_connect,
		                   commands.CONNECT_VERIFY: self.parse_connect_verify}
		if self.command != 0:
			command_parsers[self.command](data[8:])

	def parse_connect(self, remaining_data):
		self.parse_connect_verify(remaining_data)

	def parse_connect_verify(self, remaining_data):
		self.outgoing_peer_id, self.incoming_sess_id, self.outgoing_sess_id, self.mtu, self.window_size, self.channel_count, self.incoming_bandwidth, self.outgoing_bandwidth, self.packet_throttle_interval, self.packet_throttle_acceleration, self.packet_throtle_deceleration, self.connect_id = struct.unpack_from('hbbiiiiiiiii', remaining_data)

