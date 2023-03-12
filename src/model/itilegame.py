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
