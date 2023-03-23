import pygame
from src.view.render.irender import IRender
import src.common.constants as Constants



class TetrisRender(IRender):
    def __init__(self):
        self.isinitialized = False
        self.screen = None
        # self.font = None
        # self.background = pygame.Surface((Constants.S_WIDTH, Constants.S_HEIGHT))
        # self.background.fill((0, 0, 0))

    def render(self, game_model):
        # print("Rendering Tetris...")
        # screen = pygame.display.get_surface()
        # print(game_model)
        self.draw_window(game_model.grid, self.screen, game_model.score.get_score(), game_model.level)
        self.draw_next_shape(game_model.next_piece, self.screen)
        pygame.display.update()

    def initialize(self, screen):
        pygame.font.init()
        # pygame.display.set_caption("Tile Games - Tetris")
        self.screen = screen
        self.font = pygame.font.SysFont('comicsans', 60, bold=True)
        self.isinitialized = True

    def draw_window(self, grid, screen, score, level):
        screen.fill((0, 0, 0))
        # screen.blit(self.background, (0, 0))

        font = pygame.font.SysFont('comicsans', 55)
        label = font.render("Tetris", 1, (255, 255, 255))
        screen.blit(label, (Constants.TOP_LEFT_X +
                    Constants.PLAY_WIDTH / 2 - (label.get_width() / 2), 30))

        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Score: ' + str(score), 1, (255, 255, 255))

        sx = Constants.TOP_LEFT_X + Constants.PLAY_WIDTH + 50
        sy = Constants.TOP_LEFT_Y + Constants.PLAY_HEIGHT / 2 - 100

        screen.blit(label, (sx + 10, sy + 130))

        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Level: ' + str(level), 1, (255, 255, 255))

        sx = Constants.TOP_LEFT_X + Constants.PLAY_WIDTH + 50
        sy = Constants.TOP_LEFT_Y + Constants.PLAY_HEIGHT / 2 - 100

        screen.blit(label, (sx + 10, sy + 190))

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(screen, grid[i][j],
                                 (Constants.TOP_LEFT_X + j * 30, Constants.TOP_LEFT_Y + i * 30, 30, 30), 0)

        self.draw_grid(screen)
        pygame.draw.rect(screen, (255, 0, 0),
                         (Constants.TOP_LEFT_X, Constants.TOP_LEFT_Y, Constants.PLAY_WIDTH, Constants.PLAY_HEIGHT), 5)

    def draw_grid(self, screen):
        sx = Constants.TOP_LEFT_X
        sy = Constants.TOP_LEFT_Y
        for i in range(20):
            pygame.draw.line(screen, (128, 128, 128), (sx, sy + i * 30),
                             (sx + Constants.PLAY_WIDTH, sy + i * 30))  # horizontal lines
            for j in range(10):
                pygame.draw.line(screen, (128, 128, 128), (sx + j * 30, sy),
                                 (sx + j * 30, sy + Constants.PLAY_HEIGHT))  # vertical lines

    def draw_next_shape(self, shape, screen):
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
