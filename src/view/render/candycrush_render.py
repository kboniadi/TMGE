import pygame

import src.common.constants as Constants
from src.model.game.itilegame import ITileGame
from src.view.render.irender import IRender


class CandyCrushRender(IRender):
    def __init__(self):
        self.screen = None
        self.cursor = None

    def render(self, game_model):
        # print("Rendering Candy Crush...")
        self.draw_window(game_model.grid, game_model.cursor, self.screen,
                         game_model.score.get_score(), game_model.level)
        pygame.display.update()

    def initialize(self, screen):
        pygame.font.init()
        self.screen = screen
        self.cursor = pygame.image.load('./assets/images/selected.png')
        self.cursor = pygame.transform.scale(self.cursor, (30, 30))

    def draw_window(self, grid, cursor, screen, score, level):
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont('comicsans', 55)
        label = font.render("Candy Crush", 1, (255, 255, 255))
        screen.blit(label, (Constants.TOP_LEFT_X +
                    Constants.PLAY_WIDTH / 2 - (label.get_width() / 2), 30))

        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Score: ' + str(score), 1, (255, 255, 255))

        sx = Constants.TOP_LEFT_X + Constants.PLAY_WIDTH + 50
        sy = Constants.TOP_LEFT_Y + Constants.PLAY_HEIGHT / 2 - 100

        screen.blit(label, (sx + 10, sy + 130))

        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Moves: ' + str(level), 1, (255, 255, 255))

        sx = Constants.TOP_LEFT_X + Constants.PLAY_WIDTH + 50
        sy = Constants.TOP_LEFT_Y + Constants.PLAY_HEIGHT / 2 - 100

        screen.blit(label, (sx + 10, sy + 190))

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(
                    screen, grid[i][j], (Constants.TOP_LEFT_X + j * 30, Constants.TOP_LEFT_Y + i * 30, 30, 30), 0)

        self.draw_grid(screen)
        pygame.draw.rect(screen, (255, 0, 0), (Constants.TOP_LEFT_X,
                         Constants.TOP_LEFT_Y, Constants.PLAY_WIDTH, Constants.PLAY_HEIGHT), 5)
        screen.blit(self.cursor, (Constants.TOP_LEFT_X +
                    (30 * cursor.x), Constants.TOP_LEFT_Y + (30 * cursor.y)))

    def draw_grid(self, screen):
        sx = Constants.TOP_LEFT_X
        sy = Constants.TOP_LEFT_Y
        for i in range(20):
            pygame.draw.line(screen, (128, 128, 128), (sx, sy + i * 30),
                             (sx + Constants.PLAY_WIDTH, sy + i * 30))  # horizontal lines
            for j in range(10):
                pygame.draw.line(screen, (128, 128, 128), (sx + j * 30, sy),
                                 (sx + j * 30, sy + Constants.PLAY_HEIGHT))  # vertical lines
