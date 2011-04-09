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
		                   commands.CONNECT_VERIFY: self.parse_connect_verify,
				   commands.PING: self.parse_ping,
				   commands.BANDWIDTH_LIMIT: self.parse_bandwidth_limit,
				   commands.SEND_RELIABLE: self.parse_reliable,
				   commands.SEND_UNRELIABLE: self.parse_unreliable,
				   commands.SEND_UNSEQUENCED: self.parse_unsequenced,
				   commands.ACNOWLEDGE: self.parse_acknowledge,
				   commands.THROTTLE_CONFIGURE: self.parse_throttle_configure,
				   commands.DISCONNECT: parse_disconnect}
				   commands.BANDWIDTH_LIMIT: self.parse_bandwidth_limit}
		command_parsers[self.command](data[8:])

	def parse_connect(self, remaining_data):
		self.parse_connect_verify(remaining_data)

	def parse_connect_verify(self, remaining_data):
		self.outgoing_peer_id, self.incoming_sess_id, self.outgoing_sess_id, self.mtu, self.window_size, self.channel_count, self.incoming_bandwidth, self.outgoing_bandwidth, self.packet_throttle_interval, self.packet_throttle_acceleration, self.packet_throtle_deceleration, self.connect_id = struct.unpack_from('HBBIIIIIIIII', remaining_data)

	def parse_ping(self, remaining_data):
		if len(remaining_data) != 0:
			raise ValueError("unrecognized ping packet")

	def parse_bandwidth_limit(self, remaining_data):
		self.incoming_bandwidth, self.outgoing_bandwidth = struct.unpack_from('II', remaining_data)

	def parse_reliable(self, remaining_data):
		self.data_length = struct.unpack_from('H', remaining_data[:2])
		self.received_data = remaining_data[2:]

	def parse_unreliable(self, remaining_data):
		self.unreliable_sequence_number, self.data_length = struct.unpack_from('HH', remaining_data[:4])
		self.received_data = remaining_data[4:]

	def parse_unsequenced(self, remaining_data):
		self.unsequenced_group, self.data_length = struct.unpack_from('HH', remaining_data[:4])
		self.received_data = remaining_data[4:]
_
	def parse_acknowledge(self, remaining_data):
		self.acknowledged_reliable_sequence_number, self.acknowledged_sent_time = struct.unpack_from('HH', remaining_data)

	def parse_throttle_configure(self, remaining_data):
		self.throttle_inteval, self.throttle_acceleration, self.throttle_deceleration = struct.unpack_from('III', remaining_data)

	def parse_disconnect(self, remaining_data):
		self.received_data = struct.unpack_from('I', remaining_data)

	def parse_fragment(self, remaining_data):
		self.start_sequence_number, self.data_length, self.fragment_count, self.fragment_number, self.total_length, self.fragment_offset = struct.unpack_from('HHIIII', remaining_data[:20])
		self.received_data = remaining_data[20:]	

	def to_packed_proto_header(self):
		cmd = self.command
		if self.acknowledge:
			cmd = cmd | commands.FLAG_ACKNOWLEDGE
		if self.unsequenced:
			cmd = cmd | commands.FLAG_UNSEQUENCED
		return struct.pack('HHBBH', self.outgoing_peer_id, self.sent_time, cmd, self.channel_id, self.reliable_seq_num)

	def to_packed_connect_verify(self):
		self.command = commands.CONNECT_VERIFY
		return self.to_packed_proto_header() + struct.pack('HBBIIIIIIIII', self.outgoing_peer_id, self.incoming_sess_id, self.outgoing_sess_id, self.mtu, self.window_size, self.channel_count, self.incoming_bandwidth, self.outgoing_bandwidth, self.packet_throttle_interval, self.packet_throttle_acceleration, self.packet_throtle_deceleration, self.connect_id)

	def to_packed_ping(self):
		self.command = commands.PING
		self.acknowledge = True
		self.channel_id = 0xFF
		return self.to_packed_proto_header()

	def to_packed_bandwidth_limit(self):
		self.command = commands.BANDWIDTH_LIMIT
		self.channel_id = 0xFF
		return self.to_packed_proto_header() + struct.pack("II", self.incoming_bandwidth, self.outgoing_bandwidth)

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

