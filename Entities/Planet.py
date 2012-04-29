#Planet
import sys
sys.path.insert(0, '..')
from MovableEntity import *


class Planet(MovableEntity):
    """Planet"""
    def __init__(self, arg):
        super(Planet, self).__init__(arg)
