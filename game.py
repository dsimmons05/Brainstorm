import os
import sys
import pygame

class Game:
    def __init__(self, w, h):
        pygame.init()
        self.width = w
        self.height = h
        self.display = pygame.display.set_mode((w,h))

    def run(self):
        while True:
            # check events
            self.events()
            # update crap

            # draw crap

            # update the damn screen
            pygame.display.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                    pygame.quit()
