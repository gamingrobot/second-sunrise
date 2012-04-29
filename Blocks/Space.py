#Space.py

import Block


class Space(Block):
    def __init__(self, newX, newY, newZ):
        Block.__init__(self, newX, newY, newZ)
        self.renderTexture = 'transparent'
