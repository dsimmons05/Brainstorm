import sys
import os

import pygame

class Menu:
    def __init__(self):
        self.bg_image = pygame.image.load(os.path.join('assets', 'menu.png'))
        self.in_menu = True
        self.setup()
   
    def setup(self):
        ''' set up buttons and whatnot '''
        pass

    def run(self, display):
        while self.in_menu:
            self.events()
            display.blit(self.bg_image, (0,0))
            pygame.display.update()
        return False # makes game.gameover False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                    pygame.quit()
                if event.key == pygame.K_SPACE:
                    self.in_menu = False
