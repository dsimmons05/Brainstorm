import sys

from game import *

if __name__ == '__main__':
    if len(sys.argv) == 2:
        fps_const = float(sys.argv[1])
    else:
        fps_const = 1000.0
    game = Game(800, 600, fps_const)
    game.run()
