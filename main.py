from game import *

class Level:
    def __init__(self, path, filename, plats):
        pass

class Idea:
    def __init__(self, path, filename, breed, x, y):
        self.collision_lst = []
        self.image = {'idle': [], 'run': [], 'jump': []}
        self.x = x
        self.y = y
        if breed == 'big':
            pass
        if breed == 'small':
            pass
        if breed == 'creative':
            pass
    def check_jump(self):
        pass
    def check_move(self, dt):
        pass
    def check_punch(self, dt):
        pass
    def check_dead(self):
        pass
    def check_collision(self, level, enemies):
        pass
    def check_bump(self):
        pass

class Enemy:
    def __init__(self, breed):
        pass

if __name__ == '__main__':
    game = Game(800, 600)
    game.run()