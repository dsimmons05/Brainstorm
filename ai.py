import random
from idea import *
import pygame
import time

class Ai(Idea):
    def __init__(self, filename, x, y, w, h):
        self.will_punch = True
        self.start = time.time()
        Idea.__init__(self, filename, x, y, w, h)
    def choice(self, dt, enemies, jump, punch):
        self.dt = dt
        self.sound_jump = jump
        self.sound_punch = punch
        self.lst = enemies[:-1]
        self.targets = self.lst
        for enemy in self.targets:
            # Need to use time or something so you don't make random choices every loop
            if abs(self.rect.x - enemy.rect.x) < 200 and abs(self.rect.y - enemy.rect.y) < 100:
                choice = random.choice(['chase', 'chase'])
                if choice == 'chase':
                    self.chase(enemy)
                if choice == 'run':
                    self.run(enemy)
            else:
                self.random()
    def chase(self, target):
        if self.rect.x - target.rect.x > 0: 
            self.move(self.dt, 'left', sound=None)
        if self.rect.x - target.rect.x < 0:
            self.move(self.dt, 'right', sound=None)
        if self.rect.y - target.rect.y > 0:
            self.move(self.dt, 'up', self.sound_jump)
        if self.rect.y - target.rect.y < 0:
            self.move(self.dt, 'down', sound=None)
        if abs(self.rect.x - target.rect.x) < 64 and abs(self.rect.y - target.rect.y) < 64:
            self.can_punch()

    def run(self, chaser):
        dt = self.dt
        self.start_time += dt
        if self.start_time > 0:
            if self.rect.x - chaser.rect.x > 0: 
                self.move(self.dt, 'right', sound=None)
            if self.rect.x - chaser.rect.x < 0:
                self.move(self.dt, 'left', sound=None)
            if self.rect.y - chaser.rect.y > 0:
                self.move(self.dt, 'up', self.sound_jump)
            if self.rect.y - chaser.rect.y < 0:
                self.move(self.dt, 'down', sound=None)
    def random(self):
        choice = random.choice(['move', 'move'])
        if choice == 'move':
            self.move(self.dt, 'up', self.sound_jump)
        else:
            self.yv = 0.0
            self.xv = 0.0
    def can_punch(self):
        if time.time() - self.start > 1:
            self.punch(self.sound_punch)
            self.start = time.time()