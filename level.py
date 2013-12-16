import os

import pygame

class Wall:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect((x, y, w, h))

    def draw(self, display):
        pygame.draw.rect(display, (255,0,0), self.rect, 0)

class Level:
    def __init__(self):
        self.platforms = []
        self.image = None

    def add_platform(self, platform):
        self.platforms.append(platform)

    def draw(self, display):
        for plat in self.platforms:
            plat.draw(display)