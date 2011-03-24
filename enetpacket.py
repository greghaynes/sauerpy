# Licensed under The MIT License. See LICENSE for more details.

import struct

class EnetPacket(object):
	def __init__(self, data):
		self.ref_cnt = struct.unpack_from('i', data[:4])
		self.flags = struct.unpack_from('i', data[4:8])
		self.data = data[8:-4]
		self.size = struct.unpack_from('i', data[-4:])

