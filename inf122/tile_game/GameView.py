from iTileGame import iTileGame
from iSubscriber import iSubscriber
from iObserver import iObserver


class GameView(iTileGame, iObserver, iSubscriber):
	def __init__(self, board, score, genre):
		self.board = board
		self.score = score
		self.genre = genre

	def render_board(self):
		pass

	def render_score(self):
		pass

	def render_game_over(self):
		pass

	def handle_mouse_click(self):
		pass

	def handle_key_press(self):
		pass
