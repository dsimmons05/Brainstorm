import os
import sys

import pygame

from idea import *

class Game:
    def __init__(self, w, h):
        pygame.init()
        self.width = w
        self.height = h
        self.display = pygame.display.set_mode((w,h))
        self.clock = pygame.time.Clock()
        self.fps = 30

        self.idea = Idea('idea.png', 0, 0, 32, 32)

    def run(self):
        #! MAKE LEVEL CLASS
        level = pygame.image.load(os.path.join('assets', 'bg_pixelated.png'))
        while True:
            dt = self.clock.tick(self.fps) / 300.0
            # check events
            self.events()
            # update crap
            self.idea.update(dt)
            # clear screen then draw crap
            self.display.fill((255, 255, 255))
            self.display.blit(level, (0,0))
            self.idea.draw(self.display)
            # update the damn screen
            pygame.display.update()

    def events(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                    pygame.quit()
                if event.key == pygame.K_SPACE:
                    self.idea.punch()

        if keys[pygame.K_RIGHT]:
            self.idea.move('right')
        if keys[pygame.K_LEFT]:
            self.idea.move('left')