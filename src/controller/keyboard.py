import pygame

import src.common.constants as Constants
from src.listener.eventmanager import (EventManagerWeak, QuitEvent,
                                       StateChangeEvent, TickEvent)
from src.listener.iobserver import IObserver
from src.model.GameEngine import GameEngine


class Keyboard(IObserver):
    def __init__(self, evManager: 'EventManagerWeak', model: 'GameEngine'):
        self.evManager = evManager
        evManager.register(self)
        self.model = model

    def update(self, event):
        if isinstance(event, TickEvent):
            self.model.grid = self.model.create_grid()
            self.model.fall_time += self.model.clock.get_rawtime()
            self.model.level_time += self.model.clock.get_rawtime()

            if self.model.level_time/1000 > 4:
                self.model.level_time = 0
                if self.model.fall_speed > 0.15:
                    self.model.fall_speed -= 0.005

            # PIECE FALLING CODE
            if self.model.fall_time/1000 >= self.model.fall_speed:
                self.model.fall_time = 0
                self.model.current_piece.y += 1
                if not (self.model.valid_space()) and self.model.current_piece.y > 0:
                    self.model.current_piece.y -= 1
                    self.model.change_piece = True
            
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
        
            shape_pos = self.model.convert_shape_format(self.model.current_piece)

            # add piece to the grid for drawing
            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1:
                    self.model.grid[y][x] = self.model.current_piece.color

            # IF PIECE HIT GROUND
            if self.model.change_piece:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    self.model.locked_positions[p] = self.model.current_piece.color
                self.model.current_piece = self.model.next_piece
                self.model.next_piece = self.model.get_shape()
                self.model.change_piece = False

                # call four times to check for multiple clear rows
                if self.model.clear_rows():
                    self.model.score += 10
            
             # Check if user lost
            if self.model.check_lost():
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
            self.model.current_piece.x -= 1
            if not self.model.valid_space():
                self.model.current_piece.x += 1
        elif event.key == pygame.K_RIGHT:
            self.model.current_piece.x += 1
            if not self.model.valid_space():
                self.model.current_piece.x -= 1
        elif event.key == pygame.K_UP:
            # rotate shape
            self.model.current_piece.rotation = self.model.current_piece.rotation + \
                1 % len(self.model.current_piece.shape)
            if not self.model.valid_space():
                self.model.current_piece.rotation = self.model.current_piece.rotation - \
                    1 % len(self.model.current_piece.shape)

        if event.key == pygame.K_DOWN:
            # move shape down
            self.model.current_piece.y += 1
            if not self.model.valid_space():
                self.model.current_piece.y -= 1
    
    def keydownend(self, event):
        self.evManager.notify(QuitEvent())