import pygame
import src.common.constants as Constants
from src.listener.iobserver import IObserver
from src.listener.eventmanager import (
    EventManagerWeak,
    InitializeEvent,
    QuitEvent,
    StateChangeEvent,
    TickEvent,
)
from src.model.gameengine import GameEngine
from src.view.irender import iRender


class Canvas(IObserver):
    def __init__(
        self, evManager: "EventManagerWeak", model: "GameEngine", renderer: "iRender"
    ):
        self.evManager = evManager
        evManager.register(self)
        self.model = model
        self.renderer = renderer
        self.isinitialized = False
        self.screen = None

    def update(self, event):
        #print("Received event:", event)
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
        pygame.display.set_caption(str(self.model.game.name))
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

    def rendermenu(self):
        self.screen.fill((0, 0, 0))
        self.draw_text_middle('Press space key to begin.', 60, (255, 255, 255))
        pygame.display.flip()

    def renderGameOver(self):
        self.draw_text_middle("You Lost", 40, (255, 255, 255))
        pygame.display.update()

