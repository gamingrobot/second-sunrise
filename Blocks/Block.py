#Base Class : Block


"""class Block:
    #Block is a modifyable object
    def __init__(self, args):
        self.x = args['x']
        self.y = args['y']
        self.z = args['z']
        self.texture = 'Blocks/' + args['texture']
        self.density = args['density']

    def getDensity(self):
        return self.density

    def __str__(self):
        return "Block: %s is at (%i, %i, %i)" % (self.__class__.__name__, self.x, self.y, self.z)"""


class Block:
    block_id = 0
    density = 0
    hermite = []
