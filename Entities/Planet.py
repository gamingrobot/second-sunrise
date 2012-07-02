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
        self.playerchunk = self.genHash(spl[0], spl[1], spl[2])
        #generate chunk
        self.generateChunks(spl[0], spl[1], spl[2])

        #place player
        playerspl = Vec3(spl[0] + 4, spl[1] + 4, spl[2] + self.chunkSize + 4)
        player.setPos(playerspl)
        player.currentchunk = self.playerchunk

    def addChunk(self, x, y, z):
        nchunk = Chunk({'x': x, 'y': y, 'z': z,
            'planetNode': self.planetNode, 'root': self.root, 'planet': self})
        nchunk.generateBlocks(self)
        #print nchunk.getChunkID()
        self.chunks[nchunk.getChunkID()] = nchunk

    def generateChunkMesh(self, x, y, z):
        if self.debug:
            self.chunks[self.genHash(x, y, z)].generateVoxel()
        else:
            self.chunks[self.genHash(x, y, z)].generateMarching(self.chunks)

    def generateChunkBlocks(self, x, y, z):
        #generate only positive chunks and check if they are already in the tree
        if not self.genHash(x, y, z) in self.chunks:
            self.addChunk(x, y, z)
        #x y
        if not self.genHash(x + 16, y, z) in self.chunks:
            self.addChunk(x + 16, y, z)              # (x + 1, y, z)
        if not self.genHash(x + 16, y + 16, z) in self.chunks:
            self.addChunk(x + 16, y + 16, z)         # (x + 1, y + 1, z)
        if not self.genHash(x, y + 16, z) in self.chunks:
            self.addChunk(x, y + 16, z)              # (x, y + 1, z)
        #z
        if not self.genHash(x, y, z + 16) in self.chunks:
            self.addChunk(x, y, z + 16)                   # (x, y, z)
        if not self.genHash(x + 16, y, z + 16) in self.chunks:
            self.addChunk(x + 16, y, z + 16)              # (x + 1, y, z)
        if not self.genHash(x + 16, y + 16, z + 16) in self.chunks:
            self.addChunk(x + 16, y + 16, z + 16)         # (x + 1, y + 1, z)
        if not self.genHash(x, y + 16, z + 16) in self.chunks:
            self.addChunk(x, y + 16, z + 16)              # (x, y + 1, z)

    def generateChunks(self, x, y, z):
        cs = self.chunkSize
        #generate blocks
        self.generateChunkBlocks(x, y, z)
        #generate naboring chunks
        #x y
        self.generateChunkBlocks(x + cs, y, z)              # (x + 1, y, z)
        self.generateChunkBlocks(x + cs, y + cs, z)         # (x + 1, y + 1, z)
        self.generateChunkBlocks(x - cs, y + cs, z)         # (x + 1, y + 1, z)
        self.generateChunkBlocks(x - cs, y - cs, z)         # (x + 1, y + 1, z)
        self.generateChunkBlocks(x + cs, y - cs, z)         # (x + 1, y + 1, z)
        self.generateChunkBlocks(x, y + cs, z)              # (x, y + 1, z)
        self.generateChunkBlocks(x - cs, y, z)              # (x + 1, y, z)
        self.generateChunkBlocks(x, y - cs, z)              # (x, y + 1, z)
        # +z
        self.generateChunkBlocks(x, y, z + cs)                   # (x, y, z)
        self.generateChunkBlocks(x + cs, y, z + cs)              # (x + 1, y, z)
        self.generateChunkBlocks(x + cs, y + cs, z + cs)         # (x + 1, y + 1, z)
        self.generateChunkBlocks(x - cs, y + cs, z + cs)         # (x + 1, y + 1, z)
        self.generateChunkBlocks(x - cs, y - cs, z + cs)         # (x + 1, y + 1, z)
        self.generateChunkBlocks(x + cs, y - cs, z + cs)         # (x + 1, y + 1, z)
        self.generateChunkBlocks(x, y + cs, z + cs)              # (x, y + 1, z)
        self.generateChunkBlocks(x - cs, y, z + cs)              # (x + 1, y, z)
        self.generateChunkBlocks(x, y - cs, z + cs)              # (x, y + 1, z)
        # -z
        self.generateChunkBlocks(x, y, z - cs)              # (x, y, z)
        self.generateChunkBlocks(x + cs, y, z - cs)              # (x + 1, y, z)
        self.generateChunkBlocks(x + cs, y + cs, z - cs)         # (x + 1, y + 1, z)
        self.generateChunkBlocks(x - cs, y + cs, z - cs)         # (x + 1, y + 1, z)
        self.generateChunkBlocks(x - cs, y - cs, z - cs)         # (x + 1, y + 1, z)
        self.generateChunkBlocks(x + cs, y - cs, z - cs)         # (x + 1, y + 1, z)
        self.generateChunkBlocks(x, y + cs, z - cs)              # (x, y + 1, z)
        self.generateChunkBlocks(x - cs, y, z - cs)              # (x + 1, y, z)
        self.generateChunkBlocks(x, y - cs, z - cs)              # (x, y + 1, z)

        #generate meshes
        self.generateChunkMesh(x, y, z)
        #generate naboring chunks
        #x y
        self.generateChunkMesh(x + cs, y, z)              # (x + 1, y, z)
        self.generateChunkMesh(x + cs, y + cs, z)         # (x + 1, y + 1, z)
        self.generateChunkMesh(x - cs, y + cs, z)         # (x + 1, y + 1, z)
        self.generateChunkMesh(x - cs, y - cs, z)         # (x + 1, y + 1, z)
        self.generateChunkMesh(x + cs, y - cs, z)         # (x + 1, y + 1, z)
        self.generateChunkMesh(x, y + cs, z)              # (x, y + 1, z)
        self.generateChunkMesh(x - cs, y, z)              # (x + 1, y, z)
        self.generateChunkMesh(x, y - cs, z)              # (x, y + 1, z)
        # +z
        self.generateChunkMesh(x, y, z + cs)                   # (x, y, z)
        self.generateChunkMesh(x + cs, y, z + cs)              # (x + 1, y, z)
        self.generateChunkMesh(x + cs, y + cs, z + cs)         # (x + 1, y + 1, z)
        self.generateChunkMesh(x - cs, y + cs, z + cs)         # (x + 1, y + 1, z)
        self.generateChunkMesh(x - cs, y - cs, z + cs)         # (x + 1, y + 1, z)
        self.generateChunkMesh(x + cs, y - cs, z + cs)         # (x + 1, y + 1, z)
        self.generateChunkMesh(x, y + cs, z + cs)              # (x, y + 1, z)
        self.generateChunkMesh(x - cs, y, z + cs)              # (x + 1, y, z)
        self.generateChunkMesh(x, y - cs, z + cs)              # (x, y + 1, z)
        # -z
        self.generateChunkMesh(x, y, z - cs)              # (x, y, z)
        self.generateChunkMesh(x + cs, y, z - cs)              # (x + 1, y, z)
        self.generateChunkMesh(x + cs, y + cs, z - cs)         # (x + 1, y + 1, z)
        self.generateChunkMesh(x - cs, y + cs, z - cs)         # (x + 1, y + 1, z)
        self.generateChunkMesh(x - cs, y - cs, z - cs)         # (x + 1, y + 1, z)
        self.generateChunkMesh(x + cs, y - cs, z - cs)         # (x + 1, y + 1, z)
        self.generateChunkMesh(x, y + cs, z - cs)              # (x, y + 1, z)
        self.generateChunkMesh(x - cs, y, z - cs)              # (x + 1, y, z)
        self.generateChunkMesh(x, y - cs, z - cs)              # (x, y + 1, z)

    def genHash(self, x, y, z):
        return str(x) + ":" + str(y) + ":" + str(z)

    def removeBlock(self, chunkid, x, y, z):
        self.chunks[chunkid].removeBlock(x, y, z)
        cord = chunkid.split(":")
        #fix so it doesnt regenerate the entire mesh/might run into artificats tho
        self.generateChunkMesh(int(cord[0]), int(cord[1]), int(cord[2]))

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
