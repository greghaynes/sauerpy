import packettypes
import packet
import asyncore
import socket

class SauerServer(asyncore.dispatcher):
	def __init__(self, host, port, serverState):
		asyncore.dispatcher.__init__(self)
		self.serverState = serverState
		self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.bind((host, port)) 
		self.packet_handlers = {packettypes.CONNECT: self.packet_connect}

	def handle_connect(self):
		print 'connection'

	def handle_read(self):
		data, addr = self.recvfrom(2048)
		p = packet.Packet(data)
		p_type = p.popInt()
		try:
			handler = self.packet_handlers[p_type]
			handler(addr, p)
		except KeyError:
			print 'Unhandled packet'

	def handle_write(self):
		pass

	def writable(self):
		return False

	def packet_connect(self, addr, p):
		print 'Connect from', addr	

