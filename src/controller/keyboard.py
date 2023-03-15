import pygame

import src.common.constants as Constants
from src.listener.eventmanager import (EventManagerWeak, QuitEvent,
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
            self.game.do_pre_tick(self.model.clock.get_rawtime())            
            for event in pygame.event.get():
                # handle window manager closing our window
                if event.type == pygame.QUIT:
                    self.evManager.notify(QuitEvent())
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.evManager.notify(StateChangeEvent(None))
                    else:
                        currentstate = self.model.state.peek()
                        if currentstate == Constants.STATE_MENU:
                            self.keydownmenu(event)
                        if currentstate == Constants.STATE_PLAY:
                            self.keydownplay(event)
                        if currentstate == Constants.STATE_END:
                            self.keydownend(event)
        
            self.game.do_post_tick()
		
            # Check if user lost
            if self.game.check_lost():
                self.evManager.notify(StateChangeEvent(Constants.STATE_END))

    def keydownmenu(self, event):
        # escape pops the menu
        if event.key == pygame.K_ESCAPE:
            self.evManager.notify(StateChangeEvent(None))
        # space plays the game
        if event.key == pygame.K_SPACE:
            self.evManager.notify(StateChangeEvent(Constants.STATE_PLAY))

    def keydownplay(self, event):
        key = event.key
        if key == pygame.K_ESCAPE:
            self.evManager.notify(StateChangeEvent(None))
        elif key == pygame.K_q:
            self.evManager.notify(StateChangeEvent(Constants.STATE_MENU))
        else:
            self.game.handle_command(key)
    
    def keydownend(self, event):
        self.evManager.notify(QuitEvent())