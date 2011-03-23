import struct

class Packet(object):
	def __init__(self, raw_data):
		self.raw_data = raw_data
	def peekInt(self):
		c  = struct.unpack_from('b', self.raw_data)
		if c == -128:
			n, nn = c.struct.unpack_from('bb', self.raw_data)
			return (n | (nn<<8))
		elif c == -127:
			n, nn, nnn, nnnn = c.struct.unpack_from('bbbb', self.raw_data)
			return (n | (nn<<8) | (nnn<<16) | (nnnn<<24))
		else:
			return c
	def popInt(self):
		ret = peekInt(self)
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

