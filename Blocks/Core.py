#Core
import sys
sys.path.insert(0, '..')
from Block import *


class Core(Block):
    """Core is the core block of a world"""
    def __init__(self, newX, newY, newZ):
        Block.__init__(self, newX, newY, newZ, 'core.png')

    def __str__(self):
        return "Core Block"
