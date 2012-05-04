#Grass.py
import sys
sys.path.insert(0, '..')
from Block import *


class Grass(Block):
    """Grass is green and kind of like dirt"""
    def __init__(self, args):
        args['texture'] = self.__class__.__name__
        Block.__init__(self, args)
