# Licensed under The MIT License. See LICENSE for more details.

import asyncore

class EnetServer(asyncore.dispatcher):
	def __init__(self):
		asyncore.dispatcher.__init__(self)

	def handle_connect(self):
		pass

	def handle_read(self):
		data, addr = self.recvfrom(2048)
		print len(data), ': ',
		for ch in data:
			print '%x' % ord(ch),
		print ''

	def handle_write(self):
		pass

	def writable(self):
		return False

