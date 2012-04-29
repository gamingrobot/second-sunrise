#MovableEntity
import sys
sys.path.insert(0, '..')
from Entity import *


class Sun(Entity):
    """MovableEntity"""
    def __init__(self, arg):
        Entity.__init__(self, arg)

    def __str__(self):
        return "A Sun"
