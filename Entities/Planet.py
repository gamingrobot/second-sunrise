#Planet
import sys
sys.path.insert(0, '..')
from MovableEntity import *


class Planet(MovableEntity):
    """Planet"""
    def __init__(self, arg):
        MovableEntity.__init__(self, arg)

    def __str__(self):
        return "A Planet"
