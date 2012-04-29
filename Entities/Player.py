#Player
import sys
sys.path.insert(0, '..')
from MovableEntity import *


class Player(MovableEntity):
    """Player"""
    def __init__(self, arg):
        super(Player, self).__init__(arg)
