# Licensed under The MIT License. See LICENSE for more details.

import struct

class SauerStream(object):
	def __init__(self, raw_data):
		self.raw_data = raw_data
	def popUChar(self):
		c = struct.unpack_from('b', self.raw_data)
		self.raw_data = self.raw_data[1:]
		return c[0]
	def peekInt(self):
		c  = struct.unpack_from('b', self.raw_data)
		if c == -128:
			return c.struct.unpack_from('<h', self.raw_data)[0]
		elif c == -127:
			return c.struct.unpack_from('<i', self.raw_data)[0]
		else:
			return c[0]
	def popInt(self):
		ret = self.peekInt()
		if ret < 128 and ret > -127:
			self.raw_data = self.raw_data[1:]
		elif ret < 0x8000 and ret >= -0x8000:
			self.raw_data = self.raw_data[3:]
		else:
			self.raw_data = self.raw_data[5:]
		return ret
	def pushInt(self, val):
		if val < 0x80 and val > -0x7f:
			self.raw_data += struct.pack('b', val)
		elif val < 0x8000 and val >= -0x8000:
			self.raw_data += '\x80' + struct.pack('<h', val)
		else:
			self.raw_data += '\x81' + struct.pack('<i', val)
	def pushString(self, val):
		for ch in val:
			self.pushInt(ord(ch))
		self.pushInt(0)

