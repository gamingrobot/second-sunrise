#Planet
import sys
sys.path.insert(0, '..')
from MovableEntity import *
#from Chunk import *


class Planet(MovableEntity):
    """Planet"""
    def __init__(self, arg, maxc):
        MovableEntity.__init__(self, arg)
        self.chunks = []
        for x in range(0, maxc):
            s = Chunk()
            self.chunks.append(s)

    def __str__(self):
        return "A Planet"
