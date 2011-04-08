# Licensed under The MIT License. See LICENSE for more details.

import commands

import struct

class EnetPacket(object):

	def __init__(self):
		pass

	def loadRawData(self, data):
		self.data = data

		# Load packet header
		self.peer_id, self.sent_time, self.command, self.channel_id, self.reliable_seq_num = struct.unpack_from('HHBBH', data)
		# extract header information 
		self.session_id = (self.peer_id & commands.HEADER_SESSION_MASK) >> commands.HEADER_SESSION_SHIFT
		header_flags = self.peer_id & commands.HEADER_FLAG_MASK
		self.peer_id = self.peer_id & ~(commands.HEADER_FLAG_MASK | commands.HEADER_SESSION_MASK)
		self.is_compressed = (header_flags & commands.HEADER_FLAG_COMPRESSED) != 0 
		# Load command flags
		self.acknowledge = (self.command & commands.FLAG_ACKNOWLEDGE) != 0
		self.unsequenced = (self.command & commands.FLAG_UNSEQUENCED) != 0
		# Mask command out from flags
		self.command = self.command & 0xF
		# Call parser for specific packet command
		command_parsers = {commands.CONNECT: self.parse_connect,
		                   commands.CONNECT_VERIFY: self.parse_connect_verify}
		if self.command != 0:
			command_parsers[self.command](data[8:])

	def parse_connect(self, remaining_data):
		self.parse_connect_verify(remaining_data)

	def parse_connect_verify(self, remaining_data):
		self.outgoing_peer_id, self.incoming_sess_id, self.outgoing_sess_id, self.mtu, self.window_size, self.channel_count, self.incoming_bandwidth, self.outgoing_bandwidth, self.packet_throttle_interval, self.packet_throttle_acceleration, self.packet_throtle_deceleration, self.connect_id = struct.unpack_from('HBBIIIIIIIII', remaining_data)

	def toPackedProtoHeader(self):
		cmd = self.command
		if self.acknowledge:
			cmd = cmd | commands.FLAG_ACKNOWLEDGE
		if self.unsequenced:
			cmd = cmd | commands.FLAG_UNSEQUENCED
		return struct.pack('HHBBH', self.outgoing_peer_id, self.sent_time, cmd, self.channel_id, self.reliable_seq_num)

	def toPackedConnectVerify(self):
		self.command = commands.CONNECT_VERIFY
		return self.toPackedProtoHeader() + struct.pack('HBBIIIIIIIII', self.outgoing_peer_id, self.incoming_sess_id, self.outgoing_sess_id, self.mtu, self.window_size, self.channel_count, self.incoming_bandwidth, self.outgoing_bandwidth, self.packet_throttle_interval, self.packet_throttle_acceleration, self.packet_throtle_deceleration, self.connect_id)

	def __str__(self):
		ret = ''
		ret += 'Header:\n'
		ret += '\tcompressed: %d\n' % self.is_compressed
		ret += '\tpeer id: %d\n' % self.peer_id
		ret += '\tsession id: %d\n' % self.session_id
		ret += '\tcommand: %d\n' % self.command
		ret += 'Command Header:\n'
		ret += '\toutgoing peer id: %d\n' % self.outgoing_peer_id
		ret += '\tincoming session id: %d\n' % self.incoming_sess_id
		ret += '\toutgoing session id: %d\n' % self.outgoing_sess_id
		ret += 'Raw: '
		for ch in self.data:
			ret += '%x ' % ord(ch)
		return ret

