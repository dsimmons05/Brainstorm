import os

import pygame

class Idea:
    def __init__(self, filename, x, y, w, h):
        # set position and dimensions
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        # set up idea image and animation properties
        self.rect = pygame.Rect((x, y, w, h))
        self.images = {'idle': [0,1], 'run': [2,5], 'jump': [6,7]}
        self.image_frames = {} # holds number of frames for each animation
        self.split_images('idea', os.path.join('assets', filename), w, h)
        self.image = 'idle' # current image
        self.frame = 0
        self.image_speeds = {'idle': 1.0, 'run': 0.3, 'jump': 1.0}
        self.anim_time = 0.0 # keeps track of time spent on current frame
        # set up fist image and animation properties
        self.fist_images = []
        self.fist_rect = pygame.Rect(x, y, 16, 16)
        self.fist_frames = 4 # number of frames in animation
        self.fist_frame = 0 # current punching frame
        self.fist_speed = 0.1
        self.fist_anim_time = 0.0
        self.split_images('fist', os.path.join('assets', 'fist.png'), 16, 16)
        # other properties
        self.xv = 0.0
        self.facing = 1
        self.xspeed = 4.0
        self.punching = False

    def update(self, dt):
        self.animate(dt)
        self.set_image()
        self.rect = self.rect.move(self.xv, 0)
        self.xv -= cmp(self.xv, 0) * 0.1
        if abs(self.xv) < 0.2:
            self.xv = 0.0
        # punching stuff
        if self.punching:
            self.fist_rect.x = self.facing * 30 + self.rect.center[0] - max(self.facing, 0) * 16
            self.fist_rect.y = self.y + 5

    def draw(self, display):
        display.blit(pygame.transform.flip(\
                    self.images[self.image][self.frame],\
                    self.facing==-1, False),\
                    (self.rect))
        if self.punching:
            display.blit(pygame.transform.flip(\
                        self.fist_images[self.fist_frame],\
                        self.facing==-1, False),\
                        (self.fist_rect))

    def move(self, d=None): # d = direction
        if d == 'right':
            self.xv = self.xspeed
        if d == 'left':
            self.xv = -self.xspeed

    def punch(self):
        #! check if can punch
        self.punching = True
        self.fist_anim_time = 0.0

    def set_image(self):
        ''' sets image depending on x velocity and y velocity '''
        if abs(self.xv) > 1.0:
            if self.image != 'run':
                self.image = 'run'
                self.frame = 0
            self.facing = cmp(self.xv, 0)
        else:
            if self.image != 'idle':
                self.image = 'idle'
                self.frame = 0
                self.anim_time = 0.0

    def animate(self, dt):
        # change to next frame
        if self.anim_time >= self.image_speeds[self.image]:
            # reset to zero if at last frame
            if self.frame >= self.image_frames[self.image]:
                self.frame = 0
            else:
                self.frame += 1
            self.anim_time = 0.0
        # update frame time
        self.anim_time += dt
        if self.punching:
            if self.fist_anim_time >= self.fist_speed:
                if self.fist_frame >= self.fist_frames - 1:
                    self.fist_frame = 0
                    self.punching = False
                else:
                    self.fist_frame += 1
                self.fist_anim_time = 0.0
            self.fist_anim_time += dt

    def split_images(self, obj, path, w, h):
        img = pygame.image.load(path).convert_alpha()
        # split spritesheet into multiple images
        if obj == 'idea':
            # set up idle animation
            for anim in self.images.keys():
                imgs = []
                for i in range(self.images[anim][0], self.images[anim][1]+1):
                    imgs.append(img.subsurface(\
                                (i*self.w, 0),\
                                (self.w, self.h)))
                self.images[anim] = imgs
                self.image_frames[anim] = len(imgs)-1
        elif obj == 'fist':
            # set up idle animation
            for i in range(self.fist_frames):
                frame = img.subsurface(\
                            (i*16, 0),\
                            (16, 16))
                self.fist_images.append(frame)