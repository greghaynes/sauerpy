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
			print 'Sending info packet to ', addr
			p.putInt(len(self.serverState.players))
			p.putInt(5)
			p.putInt(settings.protocol_version)
			p.putInt(self.serverState.match.game_mode)
			p.putInt(int(self.serverState.match.secondsRemaining() / 60))
			p.putInt(self.serverState.max_clients)
			p.putInt(self.serverState.master_mode)

	def handle_write(self):
		pass

	def writable(self):
		return False

