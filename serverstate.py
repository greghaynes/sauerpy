import settings
import match

class ServerState(object):
	def __init__(self):
		self.players = []
		self.server_desc = settings.server_desc
		self.master_mode = settings.master_mode
		self.max_clients = settings.max_clients
		self.current_match = match.Match(self)

