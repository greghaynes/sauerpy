import settings
import match

class ServerState(object):
	def __init__(self):
		self.players = []
		self.master_mode = settings.master_mode
		self.current_match = match.Match(self)

