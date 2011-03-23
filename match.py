import settings
import time

class Match(object):
	def __init__(self, server_state, game_mode=settings.game_mode, game_map=settings.start_map):
		self.server_state = server_state
		self.game_mode = game_mode
		self.game_map = game_map
		self.start_time = time.time()
		
		self.end_time = self.start_time + settings.match_length
		self.paused = True
		self.time_remaining = 600
	def secondsRemaining(self):
		if self.paused:
			return self.time_remaining
		else:
			return self.end_time - time.time()

