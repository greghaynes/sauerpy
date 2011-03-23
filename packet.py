import struct

class Packet(object):
	def __init__(raw_data):
		self.raw_data = raw_data
	def peekInt(self):
		c  = struct.unpack_from('b', self.raw_data)
		if c == -128:
			n, nn = c.struct.unpack_from('bb', self.raw_data)
			return (n | (nn<<8))
		else if c == -127:
			n, nn, nnn = c.struct.unpack_from('bbb', self.raw_data)
			return (n | (nn<<8) | (nnn<<16))
		else
			return c
	def popInt(self):
		ret = peekInt(self)
		if ret < 128 and ret > -127:
			self.raw_data = self.raw_data[1:]
		else if ret < 0x8000 and ret >= -0x8000:
			self.raw_data = self.raw_data[4:]
		else:
			self.raw_data = self.raw_data[5:]
		return ret

