import sys
import os

import pygame

class Menu:
    def __init__(self):
        self.font = pygame.font.Font(None, 14)
        self.bg_image = pygame.image.load(os.path.join('assets', 'menu.png'))
        self.setup()

    def setup(self):
        self.in_menu = True
        self.chosen  = {'mode': None,\
                        'level': None,\
                        'players': {'p1': None, 'p2': None},\
                        'ai': 0}
        self.can_start = False # only True if level chosen and at least two ideas (ai/player)
        self.p1 = [1, 0] # start selection on mode select
        self.p2 = [4, 0] # start selection on character select
        self.options = [[], [], [], [], [], []]
        self.action = False
        ''' set up buttons and whatnot '''
        # add quit button
        self.add_button('settings', 'quit', 'QUIT')
        # add mode buttons
        self.add_button('mode', 'rounds', 'ROUNDS')
        # add level text and options
        self.add_button('level', 'brain', 'BRAIN')
        # add ai text and options
        self.add_button('ai', 0, '0')
        self.add_button('ai', 1, '1')
        self.add_button('ai', 2, '2')
        self.add_button('ai', 3, '3')
        # add character selection options
        self.add_button('character', 'idea', 'IDEA')
        # add play button
        self.add_button('start', 'start', 'START')

    def add_button(self, category, action, text='', image=None):
        _dict = {'settings': 0, 'mode': 1, 'level': 2, 'ai': 3, 'character': 4, 'start': 5}
        row = _dict[category]
        col = len(self.options[_dict[category]])
        new_button = Button(self.font, action, row, col, text, image)
        self.options[row].append(new_button)

    def run(self, display):
        while self.in_menu:
            self.events()
            display.blit(self.bg_image, (0,0))
            for row in self.options:
                for button in row:
                    button.check_select(self.p1, self.p2)
                    button.draw(display)
            pygame.display.update()
        return False # makes game.gameover False

    def events(self):
        if self.action == 'quit':
            sys.exit()
            pygame.quit()
        if self.action == 'start':
            self.in_menu = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                    pygame.quit()
                # menu navigation
                if event.key == pygame.K_RIGHT:
                    self.move(self.p1, 'right')
                if event.key == pygame.K_LEFT:
                    self.move(self.p1, 'left')
                if event.key == pygame.K_DOWN:
                    self.move(self.p1, 'down')
                if event.key == pygame.K_UP:
                    self.move(self.p1, 'up')
                if event.key == pygame.K_d:
                    self.move(self.p2, 'right')
                if event.key == pygame.K_a:
                    self.move(self.p2, 'left')
                if event.key == pygame.K_s:
                    self.move(self.p2, 'down')
                if event.key == pygame.K_w:
                    self.move(self.p2, 'up')
                # menu selection
                if event.key == pygame.K_SPACE:
                    self.choose(self.p1, 1)
                if event.key == pygame.K_LSHIFT:
                    self.choose(self.p2, 2)

    def choose(self, loc, player):
        _dict = {0: 'settings', 1: 'mode', 2: 'level', 3: 'ai', 4: 'character', 5: 'start'}
        row = _dict[loc[0]]
        # set 'chosen' for all options in row to False
        for option in self.options[loc[0]]:
            option.chosen = False
        # set 'chosen' for chosen option to True
        option = self.options[loc[0]][loc[1]]
        option.chosen = True
        self.action = option.action
        if row == 'character':
            if player == 1:
                self.chosen['players']['p1'] = self.action
            elif player == 2:
                self.chosen['players']['p2'] = self.action
        elif row == 'ai':
            self.chosen['ai'] = self.action
        elif row == 'level':
            self.chosen['level'] = self.action
        elif row == 'mode':
            self.chosen['mode'] = self.action

    def move(self, player, d):
        ''' Moves a player's selection in a direction. '''
        _dict = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
        player[0] += _dict[d][0]
        player[1] += _dict[d][1]
        if player[0] > len(self.options) - 1:
            player[0] = 0
        elif player[0] < 0:
            player[0] = len(self.options) - 1
        if player[1] > len(self.options[player[0]]) - 1:
            player[1] = 0
        elif player[1] < 0:
            player[1] = len(self.options[player[0]]) - 1

class Button:
    def __init__(self, font, action, row, col, text, image, color=(0,0,0)):
        padding = 20
        space = 70 # arbitrary amount of space between things
        btn_size = 64
        self.row, self.col = row, col
        self.text = font.render(text, 1, color)
        size = font.size(text) 
        if image != None:
            self.image = pygame.image.load(os.path.join('assets', image))
            self.image_pos = (col * space + padding, row * space + padding)
        else:
            self.image = None
        self.rect = pygame.Rect(col * space + padding, row * space + padding, btn_size, btn_size)
        self.text_pos = (self.rect.center[0] - size[0]/2, self.rect.center[1] - 5) # center text inside button
        self.selected = 0 
        self.chosen = False
        self.action = action

    def draw(self, display):
        if self.image != None:
            display.blit(self.image, self.image_pos)
        display.blit(self.text, self.text_pos)
        if self.selected == 1:
            color = (200, 32, 32)
        elif self.selected == 2:
            color = (32, 200, 32)
        elif self.selected == 3:
            color = (200, 200, 32)
        elif self.chosen: 
            color = (32, 32, 200)
        else:
            color = (200, 200, 200)
        pygame.draw.rect(display, color, self.rect, 5)

    def check_select(self, p1, p2):
        loc = [self.row, self.col]
        if loc == p1:
            if loc == p2:
                self.selected = 3
            else:
                self.selected = 1
        elif loc == p2:
            self.selected = 2
        else:
            self.selected = 0
