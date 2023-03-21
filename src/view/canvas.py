import pygame
import src.common.constants as Constants
from src.listener.iobserver import IObserver
from src.listener.eventmanager import InitializeEvent, QuitEvent, StateChangeEvent, TickEvent


class Canvas:
    def __init__(self, evManager, game_model, render_instance):
        print("Initializing Canvas...")
        self.evManager = evManager
        self.game_model = game_model
        self.render_instance = render_instance
        print("Graphics object created successfully.")

        pygame.init()
        self.window = pygame.display.set_mode((Constants.S_WIDTH, Constants.S_HEIGHT))
        pygame.display.set_caption("Tile Games")
        self.background = pygame.Surface((Constants.S_WIDTH, Constants.S_HEIGHT))
        self.background.fill((0, 0, 0))

    def update(self, event):
        if isinstance(event, TickEvent):
            print("Received TickEvent")
            self.render_instance.render(self.window)
        if isinstance(event, InitializeEvent):
            self.render_instance.render(self.window)
        if isinstance(event, StateChangeEvent) or isinstance(event, QuitEvent):
            self.render_instance.render(self.window)

    def run(self):
        print("Running Canvas...")
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.evManager.post(QuitEvent())
                elif event.type == pygame.KEYDOWN:
                    self.evManager.post(event)
            self.evManager.post(TickEvent())
            self.render_instance.render(self.screen)
            self._clock.tick(Constants.FPS)
            pygame.display.flip()

