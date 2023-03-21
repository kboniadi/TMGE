import random
from src.model.itilegame import ITileGame
from src.game.Score import Score
import src.common.constants as Constants
import pygame

# SHAPE FORMATS

S = [['.....',
	  '.....',
	  '..00.',
	  '.00..',
	  '.....'],
	 ['.....',
	  '..0..',
	  '..00.',
	  '...0.',
	  '.....']]

Z = [['.....',
	  '.....',
	  '.00..',
	  '..00.',
	  '.....'],
	 ['.....',
	  '..0..',
	  '.00..',
	  '.0...',
	  '.....']]

I = [['..0..',
	  '..0..',
	  '..0..',
	  '..0..',
	  '.....'],
	 ['.....',
	  '0000.',
	  '.....',
	  '.....',
	  '.....']]

O = [['.....',
	  '.....',
	  '.00..',
	  '.00..',
	  '.....']]

J = [['.....',
	  '.0...',
	  '.000.',
	  '.....',
	  '.....'],
	 ['.....',
	  '..00.',
	  '..0..',
	  '..0..',
	  '.....'],
	 ['.....',
	  '.....',
	  '.000.',
	  '...0.',
	  '.....'],
	 ['.....',
	  '..0..',
	  '..0..',
	  '.00..',
	  '.....']]

L = [['.....',
	  '...0.',
	  '.000.',
	  '.....',
	  '.....'],
	 ['.....',
	  '..0..',
	  '..0..',
	  '..00.',
	  '.....'],
	 ['.....',
	  '.....',
	  '.000.',
	  '.0...',
	  '.....'],
	 ['.....',
	  '.00..',
	  '..0..',
	  '..0..',
	  '.....']]

T = [['.....',
	  '..0..',
	  '.000.',
	  '.....',
	  '.....'],
	 ['.....',
	  '..0..',
	  '..00.',
	  '..0..',
	  '.....'],
	 ['.....',
	  '.....',
	  '.000.',
	  '..0..',
	  '.....'],
	 ['.....',
	  '..0..',
	  '.00..',
	  '..0..',
	  '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255),
				(255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece:
	rows = 20  # y
	columns = 10  # x

	def __init__(self, column, row, shape):
		self.x = column
		self.y = row
		self.shape = shape
		self.color = shape_colors[shapes.index(shape)]
		self.rotation = 0  # number from 0-3


class Tetris(ITileGame):
	def __init__(self):
		self.locked_positions = {}  # (x,y):(255,0,0)
		self.grid = []
		self.change_piece = None
		self.current_piece = None
		self.next_piece = None
		self.score = Score()
		self.fall_time = None
		self.level_time = None
		self.fall_speed = None
		self.lines_cleared = None
		self.level = None
		self.name = ""

	def initialize(self):
		self.locked_positions = {}  # (x,y):(255,0,0)
		self.grid = self.create_grid()

		self.change_piece = False
		self.current_piece = self.get_shape()
		self.next_piece = self.get_shape()
		self.score.initialize(0, 1)
		self.fall_time = 0
		self.level_time = 0
		self.fall_speed = .08
		self.lines_cleared = 0
		self.level = 0
		self.name = "Tetris"

	def create_grid(self):
		grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]

		for i in range(len(grid)):
			for j in range(len(grid[i])):
				if (j, i) in self.locked_positions:
					c = self.locked_positions[(j, i)]
					grid[i][j] = c
		return grid

	def get_shape(self):
		global shapes, shape_colors

		return Piece(5, 0, random.choice(shapes))

	def valid_space(self):
		accepted_positions = [[(j, i) for j in range(
			10) if self.grid[i][j] == (0, 0, 0)] for i in range(20)]
		accepted_positions = [j for sub in accepted_positions for j in sub]
		formatted = self.convert_shape_format(self.current_piece)

		for pos in formatted:
			if pos not in accepted_positions:
				if pos[1] > -1:
					return False

		return True
	
	def convert_shape_format(self, shape):
		positions = []
		format = shape.shape[shape.rotation % len(shape.shape)]

		for i, line in enumerate(format):
			row = list(line)
			for j, column in enumerate(row):
				if column == '0':
					positions.append((shape.x + j, shape.y + i))

		for i, pos in enumerate(positions):
			positions[i] = (pos[0] - 2, pos[1] - 4)

		return positions


	def clear_rows(self):
		inc = 0
		for i in range(len(self.grid)-1, -1, -1):
			row = self.grid[i]
			if (0, 0, 0) not in row:
				inc += 1
				# add positions to remove from locked
				ind = i
				for j in range(len(row)):
					try:
						del self.locked_positions[(j, i)]
					except:
						continue
		if inc > 0:
			for key in sorted(list(self.locked_positions), key=lambda x: x[1])[::-1]:
				x, y = key
				if y < ind:
					newKey = (x, y + inc)
					self.locked_positions[newKey] = self.locked_positions.pop(key)
			self.lines_cleared+=inc
			if(self.lines_cleared >= 10):
				self.lines_cleared-=10
				self.level += 1
				self.score.change_multiplier(self.level)

			if inc == 1:
				self.score.add_point(40)
			elif inc == 2:
				self.score.add_point(100)
			elif inc == 3:
				self.score.add_point(300)
			elif inc == 4:
				self.score.add_point(1200)
			else:
				self.score.add_point(0)

	def check_lost(self):
		for pos in self.locked_positions:
			x, y = pos
			if y < 1:
				return True
		return False
	
	def handle_left(self):
		self.current_piece.x -= 1
		if not self.valid_space():
			self.current_piece.x += 1

	def handle_right(self):
		self.current_piece.x += 1
		if not self.valid_space():
			self.current_piece.x -= 1

	def handle_up(self):
		# rotate shape
		self.current_piece.rotation = self.current_piece.rotation + \
			1 % len(self.current_piece.shape)
		if not self.valid_space():
			self.current_piece.rotation = self.current_piece.rotation - \
				1 % len(self.current_piece.shape)

	def handle_down(self):
		# move shape down
		self.current_piece.y += 1
		if not self.valid_space():
			self.current_piece.y -= 1
	
	def handle_space(self):
		pass

	def do_pre_tick(self, time):
		self.grid = self.create_grid()
		self.fall_time += time
		self.level_time += time

		if self.level_time/1000 > 4:
			self.level_time = 0
			if self.fall_speed > 0.15:
				self.fall_speed -= 0.005

		# PIECE FALLING CODE
		if self.fall_time/1000 >= self.fall_speed:
			self.fall_time = 0
			self.current_piece.y += 1
			if not (self.valid_space()) and self.current_piece.y > 0:
				self.current_piece.y -= 1
				self.change_piece = True

	def do_post_tick(self, _):
		shape_pos = self.convert_shape_format(self.current_piece)

		# add piece to the grid for drawing
		for i in range(len(shape_pos)):
			x, y = shape_pos[i]
			if y > -1:
				self.grid[y][x] = self.current_piece.color

		# IF PIECE HIT GROUND
		if self.change_piece:
			for pos in shape_pos:
				p = (pos[0], pos[1])
				self.locked_positions[p] = self.current_piece.color
			self.current_piece = self.next_piece
			self.next_piece = self.get_shape()
			self.change_piece = False

			# call four times to check for multiple clear rows
			if self.clear_rows():
				print("seomthing")
				self.score += 10

	def draw_next_shape(self, screen, shape):
		font = pygame.font.SysFont('comicsans', 30)
		label = font.render('Next Shape', 1, (255, 255, 255))

		sx = Constants.TOP_LEFT_X + Constants.PLAY_WIDTH + 50
		sy = Constants.TOP_LEFT_Y + Constants.PLAY_HEIGHT / 2 - 100
		format = shape.shape[shape.rotation % len(shape.shape)]

		for i, line in enumerate(format):
			row = list(line)
			for j, column in enumerate(row):
				if column == '0':
					pygame.draw.rect(screen, shape.color,
									 (sx + j * 30, sy + i * 30, 30, 30), 0)

		screen.blit(label, (sx + 10, sy - 30))

	def render(self, canvas):
		canvas.draw_window(self.grid)
		canvas.draw_next_shape(self.next_piece)