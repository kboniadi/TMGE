from abc import ABC, abstractmethod

class ITileGame(ABC):
	@abstractmethod
	def initialize(self):
		pass
	
	def moveTile(tile, delta_x, delta_y):
		pass

	def addpiece():
		pass

	def getCanvas():
		pass

	def updateScore():
		pass

	def isGameOver():
		pass

	def do_pre_tick(self, time):
		pass

	def do_post_tick(self, time):
		pass

	def handle_left(self):
		pass

	def handle_right(self):
		pass

	def handle_up(self):
		pass

	def handle_down(self):
		pass
