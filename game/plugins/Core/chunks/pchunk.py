class PChunk:
    """PChunk"""
    def __init__(self, cords, abscords):
        self.cords = cords
        self.abscords = abscords
        self.terrain = None
        self.mesh = None
        self.node = None

    def setTerrain(self, terrain):
        self.terrain = terrain

    def getTerrain(self):
        return self.terrain

    def setMesh(self, mesh):
        self.mesh = mesh

    def getMesh(self):
        return self.mesh

    def setNode(self, node):
        self.node = node

    def getNode(self):
        return self.node
