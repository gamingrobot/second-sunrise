#Planet
import sys
sys.path.insert(0, '..')
from MovableEntity import *
from Chunk import *


class Planet(MovableEntity):
    """Planet"""
    def __init__(self, args):
        MovableEntity.__init__(self, args)
        self.x = args['x']
        self.y = args['y']
        self.z = args['z']
        self.size = 4  # in chunks
        self.planetNode = args['render'].attachNewNode("Planet_Gamma")
        self.planetNode.setPos(self.x, self.y, self.z)
        #init chunks
        self.chunks = np.zeros((self.size, self.size, self.size), dtype=np.object)
        self.chunkSize = 16
        it = np.nditer(self.chunks, op_flags=['readwrite'], flags=['multi_index', 'refs_ok'])
        while not it.finished:
            index = it.multi_index
            it[0] = Chunk({'x': index[0] * self.chunkSize, 'y': index[1] * self.chunkSize, 'z': index[2] * self.chunkSize, 'planetNode': self.planetNode, 'name': str(index[0]) + str(index[1]) + str(index[2])})
            it.iternext()

        it = np.nditer(self.chunks, op_flags=['readwrite'], flags=['multi_index', 'refs_ok'])
        while not it.finished:
            index = it.multi_index
            thechunk = it[0].tolist()
            thechunk.generateBlocks()
            thechunk.generateVoxel()
            it.iternext()

    def __str__(self):
        return "A Planet"
