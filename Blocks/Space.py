#Space.py
import sys
sys.path.insert(0, '..')
from Block import *


class Space(Block):
    """Space... the final frontier..."""
    def __init__(self, newX, newY, newZ):
        Block.__init__(self, newX, newY, newZ, 'none')
