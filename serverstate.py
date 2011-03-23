import settings

class ServerState(object):
	def __init__(self):
		self.players = []
		self.master_mode = settings.master_mode
		self.game_mode = settings.game_mode

