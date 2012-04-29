#Base Class : Block


class Block:
    """Block is a modifyable object"""
    def __init__(self, newX, newY, newZ, fName):
        self.x = newX
        self.y = newY
        self.z = newZ
        self.texture = 'filepath/' + fName

    def __str__(self):
        return "Block: %s is at (%i, %i, %i)" % (self.__class__.__name__, self.x, self.y, self.z)
