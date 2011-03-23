import packet
import asyncore
import socket
import collections

class BeaconServer(asyncore.dispatcher):
	def __init__(self, host, port, serverState):
		asyncore.dispatcher.__init__(self)
		self.serverState = serverState
		self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.bind((host, port)) 
		self.write_stack = collections.deque()

	def handle_connect(self):
		print 'connection'

	def handle_read(self):
		data, addr = self.recvfrom(2048)
		p = packet(data)
		while True:
			print p.popInt()

	def handle_write(self):
		pass

	def writable(self):
		return False

