class Planet:
    """Planet"""
    def __init__(self, cords, name, parentnode):
        self.cords = cords
        self.planetNode = parentnode.attachNewNode(name)
        self.planetNode.setPos(cords)
        self.psize = 4  # chunks
        self.radius = (self.psize / 2)

    def getNode(self):
        return self.planetNode
