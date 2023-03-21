from abc import ABC

import pygame
from src.view.irender import iRender
import src.common.constants as Constants


class TetrisRender(iRender, ABC):
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((Constants.S_WIDTH, Constants.S_HEIGHT))
        pygame.display.set_caption("Tile Games - Tetris")

        self.background = pygame.Surface((Constants.S_WIDTH, Constants.S_HEIGHT))
        self.background.fill((0, 0, 0))

    def render(self, game_model):
        print("Rendering Tetris...")
        screen = pygame.display.get_surface()
        self.draw_window(game_model.grid, screen)
        game_model.draw_next_shape(screen, game_model.next_piece)
        pygame.display.update()

    def draw_window(self, grid, screen):
        screen.blit(self.background, (0, 0))

        font = pygame.font.SysFont('comicsans', 60)
        label = font.render("Tetris", 1, (255, 255, 255))
        screen.blit(label, (Constants.TOP_LEFT_X + Constants.PLAY_WIDTH / 2 - (label.get_width() / 2), 30))

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

    # def render_menu(self, game_model):
    #     print("Rendering Tetris menu...")
    #     screen = pygame.display.get_surface()
    #     screen.blit(self.background, (0, 0))
    #
    #     font = pygame.font.SysFont('comicsans', 60)
    #     label = font.render("Tetris", 1, (255, 255, 255))
    #     screen.blit(label, (Constants.TOP_LEFT_X + Constants.PLAY_WIDTH / 2 - (label.get_width() / 2), 30))
    #
    #     font = pygame.font.SysFont('comicsans', 30)
    #     label = font.render("Press any key to start...", 1, (255, 255, 255))
    #     screen.blit(label, (Constants.TOP_LEFT_X + Constants.PLAY_WIDTH / 2 - (label.get_width() / 2), 150))
    #
    #     pygame.display.update()
    #
    # def render_gameover(self, game_model):
    #     print("Rendering Tetris game over screen...")
    #     screen = pygame.display.get_surface()
    #     screen.blit(self.background, (0, 0))
    #
    #     font = pygame.font.SysFont('comicsans', 60)
    #     label = font.render("Game Over", 1, (255, 255, 255))
    #     screen.blit(label, (Constants.TOP_LEFT_X + Constants.PLAY_WIDTH / 2 - (label.get_width() / 2), 30))
    #
    #     # font = pygame.font.SysFont('comicsans', 30)
    #     # label = font.render("Press 'p' to Play Again", 1, (255, 255, 255))
    #     # screen.blit(label, (Constants.TOP_LEFT_X + Constants.PLAY_WIDTH / 2 - (label.get_width() / 2), 350))
    #
    #     pygame.display.update()
