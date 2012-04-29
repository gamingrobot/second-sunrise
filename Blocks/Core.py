#Core
import sys
sys.path.insert(0, '..')
from Block import *


class Core(Block):
    """Core is the core block of a world"""
    def __init__(self, args):
        args['texture'] = self.__class__.__name__
        Block.__init__(self, args)
