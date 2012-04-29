#MovableEntity
import sys
sys.path.insert(0, '..')
from Entity import *


class MovableEntity(Entity):
    """MovableEntity"""
    def __init__(self, arg):
        super(MovableEntity, self).__init__(arg)
