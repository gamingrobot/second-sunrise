#Air.py

import Block


class Air(object):
    """docstring for Air"""
    def __init__(self, newX, newY, newZ):
        Block.__init__(self, newX, newY, newZ)
        self.renderTexture = 'transparent:0.1'
