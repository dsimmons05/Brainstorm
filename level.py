import os

import pygame

class Wall:
    def __init__(self, x, y, w, h, animated=None):
        self.rect = pygame.Rect((x, y, w, h))

    def draw(self, display):
        pygame.draw.rect(display, (255,0,0), self.rect, 0)

class Level:
    def __init__(self, filename):
        self.platforms = []
        self.image = pygame.image.load(os.path.join('assets', filename)).convert_alpha()
        self.anims = {}

    def add_platform(self, platform):
        self.platforms.append(platform)

    def add_animation(self, filename, z, mode, speed):
        ''' add an image to the list of images to
        animate. lower z-indices are drawn first '''
        self.anims[z] = {'image': pygame.image.load(os.path.join('assets', filename)).convert_alpha(),\
                                'mode': mode,
                                'pos': 0,
                                'end': 0,
                                'speed': speed,
                                'dir': 1}
        if mode == 'horizontal':
            self.anims['end'] = self.anims['image'].get_width() - 800
        if mode == 'vertical':
            self.anims['end'] = self.anims['image'].get_height() - 600

    def animate(self, dt):
        for anim in self.anims:
            if anim['pos'] == anim['end']:
                anim['dir'] *= -1
            anim['pos'] += anim['speed'] * dt * anim['dir']

    def draw(self, display):
        # draw background images
        for i in range(len(self.anims)):
            if self.anims[i]['mode'] == 'vertical':
                display.blit(self.anims[i]['image'], (0, self.anims[i]['pos']))
            if self.anims[i]['mode'] == 'horizontal':
                display.blit(self.anims[i]['image'], (self.anims[i]['pos'], 0))

        # draw platforms
        for plat in self.platforms:
            plat.draw(display)