#Dirt.py
from Block import *


class Dirt(Block):
    """Dirt is, well, you know, dirty"""
    def __init__(self, args):
        args['texture'] = self.__class__.__name__
        Block.__init__(self, args)
