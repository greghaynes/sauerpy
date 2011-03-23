import struct

class Packet(object):
	def __init__(raw_data):
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
		if val > 128 and val < -127:
			raw_data += struct.pack('b', val)
		elif val < 0x8000 and val >= 0x8000:
			raw_data += struct.pack('bbb', 0x80, val&0x0F, val>>8)
		else:
			raw_data += struct.pack('bbbbb', 0x81,
			                        val&0xFF,
			                        (val>>8)&0xFF,
			                        (val>>16)&0xFF,
			                        (val>>24)&0xFF)

