from iTileGame import iTileGame
from iObserver import iObserver


class Canvas(iTileGame, iObserver):
	def __init__(self, width, height, tiles):
		self.width = width
		self.height = height
		self.tiles = tiles
	
	def get_tile(self):
		pass

	def set_tile(self):
		pass

	def swap_tile(self):
		pass

	def remove_tile(self, tile):
		pass

	def update(self):
		pass