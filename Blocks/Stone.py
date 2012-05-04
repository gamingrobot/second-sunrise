#Stone.py
import sys
sys.path.insert(0, '..')
from Block import *


class Stone(Block):
    """Stone is a basic building block"""
    def __init__(self, args):
        args['texture'] = self.__class__.__name__
        Block.__init__(self, args)
