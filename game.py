import os
import sys
import random
import time

import pygame

from idea import *
from level import *
from triangle import *
from ai import *

class Game:
    def __init__(self, w, h):
        pygame.init()
        self.width = w
        self.height = h
        self.display = pygame.display.set_mode((w,h))
        self.clock = pygame.time.Clock()
        self.fps = 60
        # create level
        self.level = Level('bg0.png')
        self.level.add_platform(Wall(200, 415, 460, 200))
        self.level.add_platform(Wall(320, 295, 230, 10))
        self.level.add_platform(Wall(105, 182, 260, 10))
        self.level.add_platform(Wall(505, 185, 215, 10))
        self.level.add_animation('bg1.png', 0, 'vertical', 3.0)
        self.level.add_animation('bg2.png', 1, 'horizontal', 5.0)
        # score crap
        self.font = pygame.font.Font(None, 96)
        self.score_p1 = 0
        self.score_p2 = 0
        # sound crap
        self.sound_jump = pygame.mixer.Sound(os.path.join('assets', 'jump.wav'))
        self.sound_punch = pygame.mixer.Sound(os.path.join('assets', 'punch.wav'))
        self.sound_hit = pygame.mixer.Sound(os.path.join('assets', 'hit.wav'))
        self.sound_restart = pygame.mixer.Sound(os.path.join('assets', 'restart.wav'))
        self.sound_jump.set_volume(0.5)
        self.sound_punch.set_volume(0.5)
        self.sound_hit.set_volume(0.5)
        self.sound_restart.set_volume(0.5)
        pygame.mixer.music.load(os.path.join('assets', 'brainblast.wav'))
        pygame.mixer.music.play(-1)

    def create_players(self):
        self.sound_restart.play()
        self.player = Idea('idea_yellow.png', 300, 300, 64, 64)
        self.player2 = Idea('idea_green.png', 450, 300, 64, 64)
        self.dummy = Ai('idea_yellow.png', 250, 100, 64, 64)
        self.ideas = []
        self.dead_idea = []
        self.ideas.append(self.player)
        self.ideas.append(self.player2)
        self.ideas.append(self.dummy)
        self.num_ideas = len(self.ideas)

    def run(self):
        self.menu()
        while True:
            #dt = self.clock.tick(self.fps) / 1000.0
            dt = .037
            # check events
            self.events(dt)
            # draw and update
            self.level.draw(self.display)
            self.level.animate(dt)
            self.collisions()
            self.draw_arrows()
            self.dummy.choice(dt, self.ideas, self.sound_jump, self.sound_punch)
            for idea in self.ideas:
                idea.update(dt, self.level)
                idea.draw(self.display)
                if idea.rect.x < -200 or idea.rect.x > 1000 or idea.rect.y > 1000:
                    if not idea.dead:
                        idea.dead = True
                        self.dead_idea.append(idea)
                        if idea == self.player:
                            self.score_p2 += 1
                        elif idea == self.player2:
                            self.score_p1 += 1
            self.draw_score()
            # reset game when one player left
            if len(self.dead_idea) >= self.num_ideas - 1:
                self.create_players()
            # update the damn screen
            pygame.display.update()

    def menu(self):
        menu_image = pygame.image.load(os.path.join('assets', 'menu.png'))
        while True:
            self.display.blit(menu_image, (0,0))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                        pygame.quit()
                    if event.key == pygame.K_SPACE:
                        self.create_players()
                        return
            pygame.display.update()


    def events(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.player2.move(dt, 'right')
        if keys[pygame.K_a]:
            self.player2.move(dt, 'left')
        if keys[pygame.K_w]:
            self.player2.move(dt, 'up', self.sound_jump)
        if keys[pygame.K_s]:
            self.player2.move(dt, 'down')

        if keys[pygame.K_RIGHT]:
            self.player.move(dt, 'right')
        if keys[pygame.K_LEFT]:
            self.player.move(dt, 'left')
        if keys[pygame.K_UP]:
            self.player.move(dt, 'up', self.sound_jump)
        if keys[pygame.K_DOWN]:
            self.player.move(dt, 'down')

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                    pygame.quit()
                if event.key == pygame.K_SPACE:
                    self.player.punch(self.sound_punch)
                if event.key == pygame.K_LSHIFT:
                    self.player2.punch(self.sound_punch)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.player.phasing = False
                if event.key == pygame.K_s:
                    self.player2.phasing = False

    def draw_score(self):
        self.display.blit(self.font.render(str(self.score_p1), 1, (252, 252, 97)), (310, 500))
        self.display.blit(self.font.render(str(self.score_p2), 1, (119, 252, 97)), (460, 500))

    def collisions(self):
        check_ideas = []
        for num, i in enumerate(self.ideas):
            for e in range(num+1, self.num_ideas):
                check_ideas.append([i, self.ideas[e]])
        for i1, i2 in check_ideas:
            if i1.rect.colliderect(i2.rect):
                ## might take out this requirment
                ##if abs(i1.xv) > 1.5 or abs(i2.xv) > 1.5:
                new_xv1 = (i1.xv * (i1.mass - i2.mass) + 2 * i1.mass * i2.xv) / (i1.mass + i2.mass)
                new_xv2 = (i2.xv * (i2.mass - i1.mass) + 2 * i2.mass * i1.xv) / (i2.mass + i1.mass)
                i1.xv = new_xv1
                i2.xv = new_xv2
                ## Potentials fixes
                if abs(i1.rect.x - i2.rect.x) < 46:
                        i1.rect.x -= 10
                if abs(i1.rect.y - i2.rect.y) > 64:
                    if i1.rect.y > i2.rect.y:
                        i1.rect.x -= 10
                    else:
                        i2.rect.x += 10
                if i1.bottom:
                    if not i2.bottom:
                        i2.yv = -i2.mass
                elif i2.bottom:
                    if not i1.bottom:
                        i1.yv = -i1.mass
                else:
                    new_yv1 = (i1.yv * (i1.mass - i2.mass) + 2 * i1.mass * i2.yv) / (i1.mass + i2.mass)
                    new_yv2 = (i2.yv * (i2.mass - i1.mass) + 2 * i2.mass * i1.yv) / (i2.mass + i1.mass)
                    i1.yv = new_yv1
                    i2.yv = new_yv2
            if i1.fist_rect.colliderect(i2.rect):
                if i1.punching:
                    self.sound_hit.play()
                    i2.xv = (i2.mass / 10.0) * i1.facing * i2.damage * abs(i1.xv) / 2
                    i2.yv = - (i2.mass / 10.0) * i2.damage * 5
                    ## make you move back after you punch
                    i1.xv = (i1.mass / 10.0) * (-i1.facing) * abs(i1.xv) / 2
                    i2.damage += .15
            if i2.fist_rect.colliderect(i1.rect):
                if i2.punching:
                    self.sound_hit.play()
                    i1.xv = (i1.mass / 10.0) * i2.facing * i1.damage * abs(i1.xv) / 2
                    i1.yv = - (i1.mass / 10.0) * i1.damage * 5
                    ## make you move back after you punch
                    i2.xv = (i2.mass / 10.0) * (-i2.facing) * abs(i2.xv) / 2
                    i1.damage += .15

    def draw_arrows(self):
        for idea in self.ideas:
            if idea.rect.x > self.width:
                if idea == self.player:
                    color = (252, 252, 97)
                else:
                    color = (119, 252, 97)
                arrow = Triangle(self.display, color, (self.width - 20, idea.rect.y), 10, 0, 90)
                arrow.draw()
            if idea.rect.x < 0:
                if idea == self.player:
                    color = (252, 252, 97)
                else:
                    color = (119, 252, 97)
                arrow = Triangle(self.display, color, (20, idea.rect.y), 10, 0, 270)
                arrow.draw()
            if idea.rect.y < 0:
                if idea == self.player:
                    color = (252, 252, 97)
                else:
                    color = (119, 252, 97)
                arrow = Triangle(self.display, color, (idea.rect.x, 20), 10, 0, 0)
                arrow.draw()
