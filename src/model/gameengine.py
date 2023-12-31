import random
import pygame
import src.common.constants as Constants
from src.listener.eventmanager import (EventManagerWeak, InitializeEvent,
                                       QuitEvent, StateChangeEvent, TickEvent)
from src.listener.iobserver import IObserver
from src.model.game.itilegame import ITileGame
from src.model.user import User

class GameEngine(IObserver):
    def __init__(self, evManager: 'EventManagerWeak', game: 'ITileGame', user: 'User'):
        self.evManager = evManager
        evManager.register(self)
        self.running = False
        self.state = StackMachine()
        self.game = game
        self.clock = pygame.time.Clock()
        self.user = user

    def update(self, event):
        if isinstance(event, QuitEvent):
            self.running = False
        elif isinstance(event, InitializeEvent):
            self.game.initialize()
        elif isinstance(event, StateChangeEvent):
            # pop request
            if not event.state:
                # false if no more states are left
                if not self.state.pop():
                    self.evManager.notify(QuitEvent())
            else:
                # push a new state on the stack
                self.state.push(event.state)

    def run(self):
        self.running = True
        self.evManager.notify(InitializeEvent())
        self.state.push(Constants.STATE_MENU)
        while self.running:
            self.evManager.notify(TickEvent())

    def checkmulti(self):
        return len(self.user.players) == 2


class StackMachine:
    def __init__(self):
        self.statestack = []

    def peek(self):
        try:
            return self.statestack[-1]
        except IndexError:
            return None

    def pop(self):
        try:
            self.statestack.pop()
            return len(self.statestack) > 0
        except IndexError:
            return None

    def push(self, state):
        self.statestack.append(state)
        return state
