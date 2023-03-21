import pygame

import src.common.constants as Constants
from src.listener.eventmanager import (EventManagerWeak, InitializeEvent, QuitEvent,
                                       StateChangeEvent, TickEvent)
from src.listener.iobserver import IObserver
from src.model.gameengine import GameEngine


class Keyboard(IObserver):
    def __init__(self, evManager: 'EventManagerWeak', engine: 'GameEngine'):
        self.evManager = evManager
        evManager.register(self)
        self.model = engine
        self.game = engine.game

    def update(self, event):
        if isinstance(event, TickEvent):
            current_time = self.model.clock.get_rawtime()
            currentstate = self.model.state.peek()

            if currentstate == Constants.STATE_PLAY:
                self.game.do_pre_tick(current_time)

            for event in pygame.event.get():
                # handle window manager closing our window
                if event.type == pygame.QUIT:
                    self.evManager.notify(QuitEvent())
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.evManager.notify(StateChangeEvent(None))
                    else:
                        if currentstate == Constants.STATE_MENU:
                            self.keydownmenu(event)
                        if currentstate == Constants.STATE_PLAY:
                            self.keydownplay(event)
                        if currentstate == Constants.STATE_END:
                            self.keydownend(event)

            if currentstate == Constants.STATE_PLAY:
                self.game.do_post_tick(current_time)

            # Check if user lost
            if self.game.check_lost():
                self.evManager.notify(InitializeEvent())
                self.evManager.notify(StateChangeEvent(None))

    def keydownmenu(self, event):
        # escape pops the menu
        if event.key == pygame.K_ESCAPE:
            self.evManager.notify(StateChangeEvent(None))
        # space plays the game
        if event.key == pygame.K_SPACE:
            self.evManager.notify(StateChangeEvent(Constants.STATE_PLAY))

    def keydownplay(self, event):
        key = event.key
        if key == pygame.K_LEFT:
            self.game.handle_left()
        elif key == pygame.K_RIGHT:
            self.game.handle_right()
        elif key == pygame.K_UP:
            self.game.handle_up()
        elif key == pygame.K_DOWN:
            self.game.handle_down()
        elif key == pygame.K_SPACE:
            self.game.handle_space()

    def keydownend(self, event):
        self.evManager.notify(QuitEvent())
