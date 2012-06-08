#Planet
import sys
sys.path.insert(0, '..')
from MovableEntity import *
from Chunk import *
from panda3d.core import Vec3


class Planet(MovableEntity):
    """Planet"""
    def __init__(self, args):
        MovableEntity.__init__(self, args)
        self.x = args['x']
        self.y = args['y']
        self.z = args['z']
        self.root = args['root']
        self.planetNode = args['render'].attachNewNode("Planet_Gamma")
        self.planetNode.setPos(self.x, self.y, self.z)
        #init chunks
        self.chunkSize = 16
        self.chunks = {}
        self.psize = 64  # in chunks
        self.radius = self.chunkSize * (self.psize / 2)

        model = self.root.loader.loadModel('models/box.egg')
        model.reparentTo(self.planetNode)
        model.setPos(0, 0, 0)

    def __str__(self):
        return "A Planet"

    def getCenter(self):
        d = self.size * self.chunkSize
        r = d / 2
        return self.x + r, self.y + r, self.z + r

    def spawnPlayer(self, player):
        cs = self.chunkSize
        #find a surface chunk
        spl = (0 * cs, 0 * cs, ((self.psize / 2) - 1) * cs)
        print spl
        #generate chunk
        self.addChunk(spl[0], spl[1], spl[2], True)

        #generate naboring chunks
        #x y
        self.addChunk(spl[0] + 16, spl[1], spl[2], False)              # (x + 1, y, z)
        self.addChunk(spl[0] + 16, spl[1] + 16, spl[2], False)         # (x + 1, y + 1, z)
        self.addChunk(spl[0] - 16, spl[1] + 16, spl[2], False)         # (x + 1, y + 1, z)
        self.addChunk(spl[0] - 16, spl[1] - 16, spl[2], False)         # (x + 1, y + 1, z)
        self.addChunk(spl[0] + 16, spl[1] - 16, spl[2], False)         # (x + 1, y + 1, z)
        self.addChunk(spl[0], spl[1] + 16, spl[2], False)              # (x, y + 1, z)
        self.addChunk(spl[0] - 16, spl[1], spl[2], False)              # (x + 1, y, z)
        self.addChunk(spl[0], spl[1] - 16, spl[2], False)              # (x, y + 1, z)

        """#generate naboring chunks
        #positive
        self.addChunk(spl[0] + 16, spl[1], spl[2])              # (x + 1, y, z)
        self.addChunk(spl[0] + 16, spl[1] + 16, spl[2])         # (x + 1, y + 1, z)
        self.addChunk(spl[0], spl[1] + 16, spl[2])              # (x, y + 1, z)
        self.addChunk(spl[0], spl[1] + 16, spl[2] + 16)         # (x, y, z + 1)
        self.addChunk(spl[0] + 16, spl[1], spl[2] + 16)         # (x + 1, y, z + 1)
        self.addChunk(spl[0] + 16, spl[1] + 16, spl[2] + 16)    # (x + 1, y + 1, z + 1)
        self.addChunk(spl[0], spl[1] + 16, spl[2] + 16)         # (x, y + 1, z + 1)
        #negitive
        self.addChunk(spl[0] - 16, spl[1], spl[2])              # (x - 1, y, z)
        self.addChunk(spl[0] - 16, spl[1] - 16, spl[2])         # (x - 1, y - 1, z)
        self.addChunk(spl[0], spl[1] - 16, spl[2])              # (x, y - 1, z)
        self.addChunk(spl[0], spl[1] - 16, spl[2] - 16)         # (x, y, z - 1)
        self.addChunk(spl[0] - 16, spl[1], spl[2] - 16)         # (x - 1, y, z - 1)
        self.addChunk(spl[0] - 16, spl[1] - 16, spl[2] - 16)    # (x - 1, y - 1, z - 1)
        self.addChunk(spl[0], spl[1] - 16, spl[2] - 16)         # (x, y - 1, z - 1)"""

        #place player
        playerspl = Vec3(spl[0], spl[1], spl[2] + self.chunkSize + 4)
        player.setPos(playerspl)

    def addChunk(self, x, y, z, spawnchunk):
        nchunk = Chunk({'x': x, 'y': y, 'z': z,
            'planetNode': self.planetNode, 'root': self.root, 'spawnchunk': spawnchunk})
        nchunk.generateBlocks(self)
        nchunk.generateVoxel()
        #thechunk.generateMarching()
        print nchunk.getChunkID()
        self.chunks[nchunk.getChunkID()] = nchunk

    def testBox(self, x, y, z):
        model = self.root.loader.loadModel('models/box.egg')
        model.reparentTo(self.planetNode)
        model.setPos(x, y, z)

    def testChunk(self):
        for i in range(-2, 2):
            for j in range(-2, 2):
                for k in range(-2, 2):
                    temp = (i * self.chunkSize, j * self.chunkSize, k * self.chunkSize)

                    testchunk = Chunk({'x': temp[0], 'y': temp[1], 'z': temp[2],
                        'planetNode': self.planetNode, 'root': self.root})
                    testchunk.generateBlocks(self)
                    testchunk.generateVoxel()

                    self.chunks[testchunk.getChunkID()] = testchunk
