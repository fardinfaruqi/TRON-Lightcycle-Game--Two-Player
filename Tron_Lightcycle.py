"""
TRON Lightcycle Game - Two Player
"""

from classes.constants import WIDTH, HEIGHT
from classes.game import Game

if __name__ == "__main__":
    game = Game(WIDTH, HEIGHT)
    game.run()