#Dirt.py

import Block


class Dirt(object):
    """docstring for Dirt"""
    def __init__(self, newX, newY, newZ):
        Block.__init__(self, newX, newY, newZ)
        self.renderTexture = "openFile(dirt.png)"
