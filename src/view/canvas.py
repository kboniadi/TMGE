import pygame

import src.common.constants as Constants
from src.listener.eventmanager import (EventManagerWeak, InitializeEvent,
                                       QuitEvent, StateChangeEvent, TickEvent)
from src.listener.iobserver import IObserver
from src.model.gameengine import GameEngine
from src.view.render.irender import IRender


class Canvas(IObserver):
    def __init__(
        self, evManager: 'EventManagerWeak', model: 'GameEngine', renderer: 'IRender'
    ):
        self.evManager = evManager
        evManager.register(self)
        self.model = model
        self.renderer = renderer
        self.isinitialized = False
        self.screen = None

    def update(self, event):
        # print("Received event:", event)
        if isinstance(event, InitializeEvent):
            self.initialize()
        elif isinstance(event, QuitEvent):
            self.isinitialized = False
            pygame.quit()
        elif isinstance(event, TickEvent):
            if not self.isinitialized:
                return
            currentstate = self.model.state.peek()
            if currentstate == Constants.STATE_MENU:
                self.rendermenu()
            elif currentstate == Constants.STATE_PLAY:
                self.renderer.render(self.model.game)
            elif currentstate == Constants.STATE_END:
                self.renderGameOver()
            # limit the redraw speed to 30 frames per second
            self.model.clock.tick(30)

    def initialize(self):
        _ = pygame.init()

        pygame.font.init()
        pygame.display.set_caption(str(self.model.game.get_name()))
        self.screen = pygame.display.set_mode(
            (Constants.S_WIDTH, Constants.S_HEIGHT)
        )
        self.renderer.initialize(self.screen)
        self.isinitialized = True

    def draw_text_middle(self, text, size, color):
        self.font = pygame.font.SysFont('comicsans', size, bold=True)
        label = self.font.render(text, 1, color)

        self.screen.blit(label, (Constants.TOP_LEFT_X + Constants.PLAY_WIDTH / 2 - (label.get_width() / 2),
                                 Constants.TOP_LEFT_Y + Constants.PLAY_HEIGHT / 2 - label.get_height() / 2))

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
        if self.model.checkmulti():
            player_one = self.model.user.players[0]
            player_two = self.model.user.players[1]
            if player_two.played is True:
                self.draw_stat_screen(player_one, player_two)
            else:
                if player_one.played is False:
                    self.screen.fill((0, 0, 0))
                    self.draw_text_middle('Player 1 - Press space key to begin.', 30, (255, 255, 255))
                    pygame.display.flip()
                else:
                    self.screen.fill((0, 0, 0))
                    self.draw_text_middle('Player 2 - Press space key to begin.', 30, (255, 255, 255))
                    pygame.display.flip()
        else:
            self.screen.fill((0, 0, 0))
            self.draw_text_middle('Player 1 - Press space key to begin.', 30, (255, 255, 255))
            pygame.display.flip()
    def renderGameOver(self):
        self.draw_text_middle("You Lost", 40, (255, 255, 255))
        pygame.display.update()