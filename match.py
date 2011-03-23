import settings

class Match(object):
	def __init__(self, game_mode=settings.game_mode, game_map=settings.start_map):
		self.game_mode = game_mode
		self.game_map = game_map

