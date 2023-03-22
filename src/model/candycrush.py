from src.model.itilegame import ITileGame
from src.game.Score import Score
import src.common.constants as Constants
import random

piece_color = [(0, 255, 0), (255, 0, 0), (0, 255, 255),
				(255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class Cursor:
	def __init__(self, col, row):
		self.x = 0
		self.y = 0

class CandyCrush(ITileGame):
	def __init__(self):
		self.grid = []
		self.name = ""
		self.score = Score()
		self.level = 0
		self.cursor = Cursor(0,0)
	
	def initialize(self):
		self.grid = self.create_grid()
		self.name = "Candy Crush"
		self.score.initialize(0,1)
		self.level = 10
		self.cursor = Cursor(0,0)

	def create_grid(self):
		grid = [[self.random_piece() for x in range(10)] for x in range(20)]
		return grid
	
	def random_piece(self):
		return random.choice(piece_color)
	
	def check_lost(self):
		if self.level == 0:
			if self.score.score < 1000:
				return True
			else:
				self.level = 10
		return False
	
	def handle_down(self):
		if self.cursor.y != 20:
			self.cursor.y +=1
	
	def handle_up(self):
		if self.cursor.y != 0:
			self.cursor.y -=1

	def handle_right(self):
		if self.cursor.x != 8:
			self.cursor.x +=1

	def handle_left(self):
		if self.cursor.x != 0:
			self.cursor.x -=1
	
	def handle_space(self):
		x = self.cursor.x
		y = self.cursor.y
		self.grid[y][x], self.grid[y][x+1] = self.grid[y][x+1], self.grid[y][x] 
		self.level -=1

	def do_pre_tick(self, time):
		if self.level != 10:
			self.check_matches()
			self.check_gaps()
			self.add_new_tiles()

	def check_matches(self):
		for y in range(20):
			for x in range(10-2):
				if self.grid[y][x] == self.grid[y][x+1] == self.grid[y][x+2]:
					self.grid[y][x] = (0,0,0)
					self.grid[y][x+1] = (0,0,0)
					self.grid[y][x+2] = (0,0,0)
					self.score.add_point(10)
		
		for y in range(20-2):
			for x in range(10):
				if self.grid[y][x] == self.grid[y+1][x] == self.grid[y+2][x]:
					self.grid[y][x] = (0,0,0)
					self.grid[y+1][x] = (0,0,0)
					self.grid[y+2][x] = (0,0,0)
					self.score.add_point(10)
	
	def check_gaps(self):
		for y in range(20-1,-1,-1):
			for x in range(10):
				if self.grid[y][x] is (0,0,0):
					self.drop_tiles(x,y)

	def drop_tiles(self,x,y):
		for row in range(y,0,-1):
			self.grid[row][x] = self.grid[row-1][x]
		self.grid[0][x] = (0,0,0)


	def add_new_tiles(self):
		for x in range(10):
			if self.grid[0][x] is (0,0,0):
				self.grid[0][x] = random.choice(piece_color)