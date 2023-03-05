from iTileGame import iTileGame
from iObserver import iObserver


class Score(iTileGame, iObserver):
	def __init__(self, score, multiplier):
		self.score = score
		self.multiplier = multiplier

	def add_point(self):
		pass

	def get_score(self):
		pass

	def reset_multiplier(self):
		pass

	def increase_multiplier(self):
		pass
