class Planet:
    """Planet"""
    def __init__(self, cords, radius, name, parentnode):
        self.cords = cords
        self.planetNode = parentnode.attachNewNode(name)
        self.planetNode.setPos(cords)
        self.psize = radius  # chunks
        self.radius = (self.psize / 2)

    def getNode(self):
        return self.planetNode
