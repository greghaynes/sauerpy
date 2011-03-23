import asyncore
import socket

class SauerServer(asyncore.dispatcher):
	def __init__(self, host, port):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.bind((host, port)) 

	def handle_connect(self):
		print 'connection'

	def handle_read(self):
		data, addr = self.recvfrom(2048)
		print str(addr)+" >> "+data

	def handle_write(self):
		pass

	def writable(self):
		return False

