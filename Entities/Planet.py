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
        self.debug = args['debug']
        self.planetNode.setPos(self.x, self.y, self.z)
        #init chunks
        self.chunkSize = 16
        self.chunks = {}
        self.psize = 16  # in chunks
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
        #spl = (0 * cs, 0 * cs, ((self.psize / 2) - 1) * cs)
        spl = (0 * cs, 0 * cs, ((self.psize / 2) - 1) * cs)

        print spl
        #generate chunk
        #self.addSpawnChunk(spl[0], spl[1], spl[2])
        self.generateChunkBlocks(spl[0], spl[1], spl[2], self.chunks, True)
        self.generateChunkBlocks(spl[0] + cs, spl[1] + cs, spl[2], self.chunks)
        self.generateChunkBlocks(spl[0] + cs, spl[1], spl[2], self.chunks)
        self.generateChunkBlocks(spl[0], spl[1] + cs, spl[2], self.chunks)

        """#generate naboring chunks
        #x spl[1]
        self.addChunk(spl[0] + 16, spl[1], spl[2])              # (x + 1, spl[1], spl[2])
        self.addChunk(spl[0] + 16, spl[1] + 16, spl[2])         # (x + 1, spl[1] + 1, spl[2])
        self.addChunk(spl[0] - 16, spl[1] + 16, spl[2])         # (x + 1, spl[1] + 1, spl[2])
        self.addChunk(spl[0] - 16, spl[1] - 16, spl[2])         # (x + 1, spl[1] + 1, spl[2])
        self.addChunk(spl[0] + 16, spl[1] - 16, spl[2])         # (x + 1, spl[1] + 1, spl[2])
        self.addChunk(spl[0], spl[1] + 16, spl[2])              # (x, spl[1] + 1, spl[2])
        self.addChunk(spl[0] - 16, spl[1], spl[2])              # (x + 1, spl[1], spl[2])
        self.addChunk(spl[0], spl[1] - 16, spl[2])              # (x, spl[1] + 1, spl[2])
        # +spl[2]
        self.addChunk(spl[0], spl[1], spl[2] + 16)                   # (x, spl[1], spl[2])
        self.addChunk(spl[0] + 16, spl[1], spl[2] + 16)              # (x + 1, spl[1], spl[2])
        self.addChunk(spl[0] + 16, spl[1] + 16, spl[2] + 16)         # (x + 1, spl[1] + 1, spl[2])
        self.addChunk(spl[0] - 16, spl[1] + 16, spl[2] + 16)         # (x + 1, spl[1] + 1, spl[2])
        self.addChunk(spl[0] - 16, spl[1] - 16, spl[2] + 16)         # (x + 1, spl[1] + 1, spl[2])
        self.addChunk(spl[0] + 16, spl[1] - 16, spl[2] + 16)         # (x + 1, spl[1] + 1, spl[2])
        self.addChunk(spl[0], spl[1] + 16, spl[2] + 16)              # (x, spl[1] + 1, spl[2])
        self.addChunk(spl[0] - 16, spl[1], spl[2] + 16)              # (x + 1, spl[1], spl[2])
        self.addChunk(spl[0], spl[1] - 16, spl[2] + 16)              # (x, spl[1] + 1, spl[2])
        # -spl[2]
        self.addChunk(spl[0], spl[1], spl[2] - 16)              # (x, spl[1], spl[2])
        self.addChunk(spl[0] + 16, spl[1], spl[2] - 16)              # (x + 1, spl[1], spl[2])
        self.addChunk(spl[0] + 16, spl[1] + 16, spl[2] - 16)         # (x + 1, spl[1] + 1, spl[2])
        self.addChunk(spl[0] - 16, spl[1] + 16, spl[2] - 16)         # (x + 1, spl[1] + 1, spl[2])
        self.addChunk(spl[0] - 16, spl[1] - 16, spl[2] - 16)         # (x + 1, spl[1] + 1, spl[2])
        self.addChunk(spl[0] + 16, spl[1] - 16, spl[2] - 16)         # (x + 1, spl[1] + 1, spl[2])
        self.addChunk(spl[0], spl[1] + 16, spl[2] - 16)              # (x, spl[1] + 1, spl[2])
        self.addChunk(spl[0] - 16, spl[1], spl[2] - 16)              # (x + 1, spl[1], spl[2])
        self.addChunk(spl[0], spl[1] - 16, spl[2] - 16)              # (x, spl[1] + 1, spl[2])"""

        #generate meshes
        self.generateChunkMesh(spl[0], spl[1], spl[2], self.chunks)
        self.generateChunkMesh(spl[0] + cs, spl[1] + cs, spl[2], self.chunks)
        self.generateChunkMesh(spl[0] + cs, spl[1], spl[2], self.chunks)
        self.generateChunkMesh(spl[0], spl[1] + cs, spl[2], self.chunks)
        """self.generateChunkMesh(self.chunks[str(spl[0] + 16) + ":" + str(spl[1]) + ":" + str(spl[2])], self.chunks)
        self.generateChunkMesh(self.chunks[str(spl[0] + 16) + ":" + str(spl[1] + 16) + ":" + str(spl[2])], self.chunks)
        self.generateChunkMesh(self.chunks[str(spl[0]) + ":" + str(spl[1] + 16) + ":" + str(spl[2])], self.chunks)
        self.generateChunkMesh(self.chunks[str(spl[0]) + ":" + str(spl[1] + 16) + ":" + str(spl[2] + 16)], self.chunks)
        self.generateChunkMesh(self.chunks[str(spl[0]) + ":" + str(spl[1]) + ":" + str(spl[2] + 16)], self.chunks)
        self.generateChunkMesh(self.chunks[str(spl[0] + 16) + ":" + str(spl[1] + 16) + ":" + str(spl[2] + 16)], self.chunks)"""

        #place player
        playerspl = Vec3(spl[0], spl[1], spl[2] + self.chunkSize + 4)
        player.setPos(playerspl)

    def addSpawnChunk(self, x, y, z):
        nchunk = Chunk({'x': x, 'y': y, 'z': z,
            'planetNode': self.planetNode, 'root': self.root, 'spawnchunk': True})
        nchunk.generateBlocks(self)
        print nchunk.getChunkID()
        self.chunks[nchunk.getChunkID()] = nchunk

    def addChunk(self, x, y, z):
        nchunk = Chunk({'x': x, 'y': y, 'z': z,
            'planetNode': self.planetNode, 'root': self.root, 'spawnchunk': False})
        nchunk.generateBlocks(self)
        print nchunk.getChunkID()
        self.chunks[nchunk.getChunkID()] = nchunk

    def generateChunkMesh(self, x, y, z, chunks):
        #print chunks
        #if chunk.spawn:
        if self.debug:
            chunks[self.genHash(x, y, z)].generateVoxel()
        else:
            chunks[self.genHash(x, y, z)].generateMarching(chunks)

    def generateChunkBlocks(self, x, y, z, chunks, spawnchunk=False):
        #generate only positive chunks and check if they are already in the tree
        if not self.genHash(x, y, z) in chunks:
            if spawnchunk:
                self.addSpawnChunk(x, y, z)
            else:
                self.addChunk(x, y, z)
        #x y
        if not self.genHash(x + 16, y, z) in chunks:
            self.addChunk(x + 16, y, z)              # (x + 1, y, z)
        if not self.genHash(x + 16, y + 16, z) in chunks:
            self.addChunk(x + 16, y + 16, z)         # (x + 1, y + 1, z)
        if not self.genHash(x, y + 16, z) in chunks:
            self.addChunk(x, y + 16, z)              # (x, y + 1, z)
        #z
        if not self.genHash(x, y, z + 16) in chunks:
            self.addChunk(x, y, z + 16)                   # (x, y, z)
        if not self.genHash(x + 16, y, z + 16) in chunks:
            self.addChunk(x + 16, y, z + 16)              # (x + 1, y, z)
        if not self.genHash(x + 16, y + 16, z + 16) in chunks:
            self.addChunk(x + 16, y + 16, z + 16)         # (x + 1, y + 1, z)
        if not self.genHash(x, y + 16, z + 16) in chunks:
            self.addChunk(x, y + 16, z + 16)              # (x, y + 1, z)

    def genHash(self, x, y, z):
        return str(x) + ":" + str(y) + ":" + str(z)

    def removeBlock(self, chunkid, x, y, z):
        self.chunks[chunkid].removeBlock(x, y, z)
        cord = chunkid.split(":")
        #fix so it doesnt regenerate the entire mesh/might run into artificats tho
        self.generateChunkMesh(int(cord[0]), int(cord[1]), int(cord[2]), self.chunks)

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
