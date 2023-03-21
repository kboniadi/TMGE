import pygame
import src.common.constants as Constants
from src.listener.iobserver import IObserver
from src.listener.eventmanager import EventManagerWeak, InitializeEvent, QuitEvent, StateChangeEvent, TickEvent
from src.model.gameengine import GameEngine
from src.model.tetris import Tetris

class Canvas(IObserver):
    def __init__(self, evManager: 'EventManagerWeak', model: 'GameEngine'):
        self.evManager = evManager
        evManager.register(self)
        self.model = model
        #Why not adding this?
        #self.game = model.game
        self.isinitialized = False
        self.screen = None
        # self.clock = None
        self.font = None

    def update(self, event):
        if isinstance(event, InitializeEvent):
            self.initialize()
        elif isinstance(event, QuitEvent):
            # shut down the pygame graphics
            self.isinitialized = False
            pygame.quit()
        elif isinstance(event, TickEvent):
            if not self.isinitialized:
                return
            currentstate = self.model.state.peek()
            if currentstate == Constants.STATE_MENU:
                self.rendermenu()
            elif currentstate == Constants.STATE_PLAY:
                self.rendergame()
            elif currentstate == Constants.STATE_END:
                self.renderGameOver()
            # limit the redraw speed to 30 frames per second
            self.model.clock.tick(30)

    def draw_text_middle(self, text, size, color):
        self.font = pygame.font.SysFont('comicsans', size, bold=True)
        label = self.font.render(text, 1, color)

        self.screen.blit(label, (Constants.TOP_LEFT_X + Constants.PLAY_WIDTH/2 - (label.get_width() / 2),
                                 Constants.TOP_LEFT_Y + Constants.PLAY_HEIGHT/2 - label.get_height()/2))

    def draw_stat_screen(self, player_one, player_two):
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('Game Stats', 1, (255, 255, 255))
        self.screen.blit(label, (Constants.TOP_LEFT_X + Constants.PLAY_WIDTH /
                                 2 - (label.get_width() / 2), 30))
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render("Player 1's Score: " + str(player_one.score), 1, (255, 255, 255))
        self.screen.blit(label, (Constants.TOP_LEFT_X + Constants.PLAY_WIDTH /
                                 2 - (label.get_width() / 2), 230))
        label = font.render("Player 2's Score: " + str(player_two.score), 1, (255, 255, 255))
        self.screen.blit(label, (Constants.TOP_LEFT_X + Constants.PLAY_WIDTH /
                                 2 - (label.get_width() / 2), 280))
        winner_text = 'It is a Tie!'
        if player_one.score > player_two.score:
            winner_text = 'Player 1 Wins!'
        elif player_two.score > player_one.score:
            winner_text = 'Player 2 Wins!'
        else:
            winner_text = 'It is a Tie!'
        label = font.render(winner_text, 1, (255, 255, 255))
        self.screen.blit(label, (Constants.TOP_LEFT_X + Constants.PLAY_WIDTH /
                                 2 - (label.get_width() / 2), 330))
        label = font.render('Press ESC to quit the game.', 1, (255, 255, 255))
        self.screen.blit(label, (Constants.TOP_LEFT_X + Constants.PLAY_WIDTH /
                                 2 - (label.get_width() / 2), 430))
        pygame.display.flip()

    def rendermenu(self):
        if self.model.checkmulti:
            player_one = self.model.user.players[0]
            player_two = self.model.user.players[1]
            if player_two.played is True:
                self.draw_stat_screen(player_one, player_two)
                '''
                # print("here")
                # self.draw_stat_screen()
                self.screen.fill((0, 0, 0))
                winner_text = None
                if player_one.score > player_two.score:
                    winner_text = 'Player 1 Wins'
                elif player_two.score > player_one.score:
                    winner_text = 'Player 2 Wins'
                else:
                    winner_text = 'It is a Tie'
                self.draw_text_middle(f'Player 1 Score: {player_one.score}. Player 2 Score: {player_two.score}.\n{winner_text}', 40, (255, 255, 255))
                pygame.display.flip()
                # ## the above goes in draw_stat_scree function
                '''
            else:
                self.screen.fill((0, 0, 0))
                self.draw_text_middle('Press space key to begin.', 60, (255, 255, 255))
                pygame.display.flip()
        else:
            self.screen.fill((0, 0, 0))
            self.draw_text_middle('Press space key to begin.', 60, (255, 255, 255))
            pygame.display.flip()

    def rendergame(self):
        #just to keep it for now
        # self.draw_window(self.model.game.grid)
        #
        # if isinstance(self.model.game, Tetris):
        #     self.model.game.draw_next_shape(self.screen, self.model.game.next_piece)
        #
        # pygame.display.update()

        self.model.game.render(self)
        pygame.display.update()

    def renderGameOver(self):
        self.draw_text_middle("You Lost", 40, (255, 255, 255))
        pygame.display.update()

    def initialize(self):
        _ = pygame.init()
        pygame.font.init()
        pygame.display.set_caption(str(self.model.game.name))
        self.screen = pygame.display.set_mode(
            (Constants.S_WIDTH, Constants.S_HEIGHT))
        # self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('comicsans', 60, bold=True)
        self.isinitialized = True


    def draw_grid(self, row, col):
        sx = Constants.TOP_LEFT_X
        sy = Constants.TOP_LEFT_Y
        for i in range(row):
            pygame.draw.line(self.screen, (128, 128, 128), (sx, sy + i*30),
                            (sx + Constants.PLAY_WIDTH, sy + i * 30))  # horizontal lines
            for j in range(col):
                pygame.draw.line(self.screen, (128, 128, 128), (sx + j * 30, sy),
                                (sx + j * 30, sy + Constants.PLAY_HEIGHT))  # vertical lines


    def draw_window(self, grid):
        self.screen.fill((0, 0, 0))
        # Tetris Title
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('TETRIS', 1, (255, 255, 255))

        self.screen.blit(label, (Constants.TOP_LEFT_X + Constants.PLAY_WIDTH /
                                 2 - (label.get_width() / 2), 30))

        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Score: ' + str(self.model.game.score.get_score()), 1, (255, 255, 255))

        sx = Constants.TOP_LEFT_X + Constants.PLAY_WIDTH + 50
        sy = Constants.TOP_LEFT_Y + Constants.PLAY_HEIGHT/2 - 100

        self.screen.blit(label, (sx + 10, sy + 130))

        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Level: ' + str(self.model.game.level), 1, (255, 255, 255))

        sx = Constants.TOP_LEFT_X + Constants.PLAY_WIDTH + 50
        sy = Constants.TOP_LEFT_Y + Constants.PLAY_HEIGHT/2 - 100

        self.screen.blit(label, (sx + 10, sy + 190))

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(
                    self.screen, grid[i][j], (Constants.TOP_LEFT_X + j * 30, Constants.TOP_LEFT_Y + i * 30, 30, 30), 0)

        # draw grid and border
        self.draw_grid(20, 10)
        pygame.draw.rect(self.screen, (255, 0, 0), (Constants.TOP_LEFT_X,
                                                    Constants.TOP_LEFT_Y, Constants.PLAY_WIDTH, Constants.PLAY_HEIGHT), 5)

        # draw any additional graphic
    # def render_next_state
    def draw_next_shape(self, shape):
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Next Shape', 1, (255, 255, 255))

        sx = Constants.TOP_LEFT_X + Constants.PLAY_WIDTH + 50
        sy = Constants.TOP_LEFT_Y + Constants.PLAY_HEIGHT/2 - 100
        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(self.screen, shape.color,
                                     (sx + j*30, sy + i*30, 30, 30), 0)

        self.screen.blit(label, (sx + 10, sy - 30))