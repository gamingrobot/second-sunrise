#Base Class : Block


class Block:
    """Block is a modifyable object"""
    def __init__(self, newX, newY, newZ):
        self.x = newX
        self.y = newY
        self.z = newZ
