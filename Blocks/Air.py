#Air.py
import sys
sys.path.insert(0, '..')
from Block import *


class Air(Block):
    """Air is a slightly transparent block that allows players to breathe"""
    def __init__(self, newX, newY, newZ):
        Block.__init__(self, newX, newY, newZ, 'air.png')
