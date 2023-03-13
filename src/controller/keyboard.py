import pygame

import src.common.constants as Constants
from src.listener.eventmanager import (EventManagerWeak, QuitEvent,
                                       StateChangeEvent, TickEvent)
from src.listener.iobserver import IObserver
from src.model.GameEngine import GameEngine


class Keyboard(IObserver):
    def __init__(self, evManager: 'EventManagerWeak', engine: 'GameEngine'):
        self.evManager = evManager
        evManager.register(self)
        self.model = engine
        self.game = engine.game

    def update(self, event):
        if isinstance(event, TickEvent):
            self.game.grid = self.game.create_grid()
            self.game.fall_time += self.model.clock.get_rawtime()
            self.game.level_time += self.model.clock.get_rawtime()

            if self.game.level_time/1000 > 4:
                self.game.level_time = 0
                if self.game.fall_speed > 0.15:
                    self.game.fall_speed -= 0.005

            # PIECE FALLING CODE
            if self.game.fall_time/1000 >= self.game.fall_speed:
                self.game.fall_time = 0
                self.game.current_piece.y += 1
                if not (self.game.valid_space()) and self.game.current_piece.y > 0:
                    self.game.current_piece.y -= 1
                    self.game.change_piece = True
            
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
        
            shape_pos = self.game.convert_shape_format(self.game.current_piece)

            # add piece to the grid for drawing
            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1:
                    self.game.grid[y][x] = self.game.current_piece.color

            # IF PIECE HIT GROUND
            if self.game.change_piece:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    self.game.locked_positions[p] = self.game.current_piece.color
                self.game.current_piece = self.game.next_piece
                self.game.next_piece = self.game.get_shape()
                self.game.change_piece = False

                # call four times to check for multiple clear rows
                if self.game.clear_rows():
                    print("seomthing")
                    self.game.score += 10
            
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
        if event.key == pygame.K_ESCAPE:
            self.evManager.notify(StateChangeEvent(None))
        elif event.key == pygame.K_q:
            self.evManager.notify(StateChangeEvent(Constants.STATE_MENU))
        elif event.key == pygame.K_LEFT:
            self.game.current_piece.x -= 1
            if not self.game.valid_space():
                self.game.current_piece.x += 1
        elif event.key == pygame.K_RIGHT:
            self.game.current_piece.x += 1
            if not self.game.valid_space():
                self.game.current_piece.x -= 1
        elif event.key == pygame.K_UP:
            # rotate shape
            self.game.current_piece.rotation = self.game.current_piece.rotation + \
                1 % len(self.game.current_piece.shape)
            if not self.game.valid_space():
                self.game.current_piece.rotation = self.game.current_piece.rotation - \
                    1 % len(self.game.current_piece.shape)

        if event.key == pygame.K_DOWN:
            # move shape down
            self.game.current_piece.y += 1
            if not self.game.valid_space():
                self.game.current_piece.y -= 1
    
    def keydownend(self, event):
        self.evManager.notify(QuitEvent())