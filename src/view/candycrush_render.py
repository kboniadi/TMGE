import pygame
from src.view.irender import iRender
import src.common.constants as Constants


class CandyCrushRender(iRender):
    def __init__(self):
        pygame.init()
        self.isinitialized = False
        self.screen = None
        self.font = None
        self.cursor = None

    def render(self, game_model):
        print("Rendering Candy Crush...")
        if not self.isinitialized:
            self.initialize()
        self.draw_window(game_model.grid, game_model.cursor, self.screen)
        pygame.display.update()

    def initialize(self):
        pygame.font.init()
        pygame.display.set_caption("Tile Games - Candy Crush")
        self.screen = pygame.display.set_mode((Constants.S_WIDTH, Constants.S_HEIGHT))
        self.font = pygame.font.SysFont('comicsans', 60, bold=True)
        self.cursor = pygame.image.load('./images/selected.png')
        self.cursor = pygame.transform.scale(self.cursor, (60, 30))
        self.isinitialized = True

    def draw_window(self, grid, cursor, screen):
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render("Candy Crush", 1, (255, 255, 255))
        screen.blit(label, (Constants.TOP_LEFT_X + Constants.PLAY_WIDTH / 2 - (label.get_width() / 2), 30))

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(screen, grid[i][j], (Constants.TOP_LEFT_X + j * 30, Constants.TOP_LEFT_Y + i * 30, 30, 30), 0)

        self.draw_grid(screen)
        pygame.draw.rect(screen, (255, 0, 0), (Constants.TOP_LEFT_X, Constants.TOP_LEFT_Y, Constants.PLAY_WIDTH, Constants.PLAY_HEIGHT), 5)
        screen.blit(self.cursor, (Constants.TOP_LEFT_X + (30 * cursor.x), Constants.TOP_LEFT_Y + (30 * cursor.y)))

    def draw_grid(self, screen):
        sx = Constants.TOP_LEFT_X
        sy = Constants.TOP_LEFT_Y
        for i in range(20):
            pygame.draw.line(screen, (128, 128, 128), (sx, sy + i * 30), (sx + Constants.PLAY_WIDTH, sy + i * 30))  # horizontal lines
            for j in range(10):
                pygame.draw.line(screen, (128, 128, 128), (sx + j * 30, sy), (sx + j * 30, sy + Constants.PLAY_HEIGHT))  # vertical lines

