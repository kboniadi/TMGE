class Score:
	def __init__(self):
		self.score = 0
		self.multiplier = 0

	def initialize(self, score, multiplier):
		self.score = score
		self.multiplier = multiplier

	def add_point(self, points):
		self.score = self.score + points*self.multiplier

	def get_score(self):
		return self.score

	def reset_multiplier(self):
		self.multiplier = 1

	def change_multiplier(self, level):
		self.multiplier = level
