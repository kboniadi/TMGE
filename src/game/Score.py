from src.model.itilegame import ITileGame
from src.listener.iobserver import IObserver


class Score(ITileGame, IObserver):
	def __init__(self):
		self.score = None
		self.multiplier = None

	def initialize(self, score, multiplier):
		self.score = score
		self.multiplier = multiplier

	def add_point(self, points):
		print(self.score, self.multiplier, points)
		self.score = self.score + points*self.multiplier

	def get_score(self):
		return self.score

	def reset_multiplier(self):
		self.multiplier = 1

	def change_multiplier(self, level):
		self.multiplier = level