#Space.py
import sys
sys.path.insert(0, '..')
from Block import *


class Space(Block):
    """Space... the final frontier..."""
    def __init__(self, args):
        args['texture'] = self.__class__.__name__
        Block.__init__(self, args)
