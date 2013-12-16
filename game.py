import os
import sys

import pygame

from idea import *
from level import *

class Game:
    def __init__(self, w, h):
        pygame.init()
        self.width = w
        self.height = h
        self.display = pygame.display.set_mode((w,h))
        self.clock = pygame.time.Clock()
        self.fps = 30
        # create ideas
        self.player = Idea('idea.png', 0, 300, 32, 32)
        self.dummy = Idea('idea.png', 150, 300, 32, 32)
        self.ideas = []
        self.ideas.append(self.player)
        self.ideas.append(self.dummy)
        # create level
        self.level = Level()
        self.level.add_platform(Wall(0, 400, 500, 10))
        self.level.add_platform(Wall(100, 500, 500, 10))

    def run(self):
        #! MAKE LEVEL CLASS
        level = pygame.image.load(os.path.join('assets', 'bg_pixelated.png'))
        while True:
            dt = self.clock.tick(self.fps) / 1000.0
            # check events
            self.events(dt)
            # update crap
        #self.player.update(dt, self.level)
            # clear screen then draw crap
            #self.display.fill((255, 255, 255))
            self.display.blit(level, (0,0))
            self.level.draw(self.display)
            for idea in self.ideas:
                idea.update(dt, self.level)
                idea.draw(self.display)
        #self.player.draw(self.display)
            # update the damn screen
            pygame.display.update()

    def events(self, dt):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                    pygame.quit()
                if event.key == pygame.K_SPACE:
                    self.player.punch()

        if keys[pygame.K_RIGHT]:
            self.player.move(dt, 'right')
        if keys[pygame.K_LEFT]:
            self.player.move(dt, 'left')
        if keys[pygame.K_UP]:
            self.player.move(dt, 'up')