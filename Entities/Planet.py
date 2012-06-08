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
        self.root = args['root']
        self.planetNode = args['render'].attachNewNode("Planet_Gamma")
        self.planetNode.setPos(self.x, self.y, self.z)
        #init chunks
        self.chunkSize = 16
        self.chunks = {}
        self.psize = 4  # in chunks

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
        #find a surface chunk
        spawnchunk = (0 * self.chunkSize, 0 * self.chunkSize, -2 * self.chunkSize)
        print spawnchunk
        #generate chunk
        thechunk = Chunk({'x': spawnchunk[0], 'y': spawnchunk[1], 'z': spawnchunk[2],
            'planetNode': self.planetNode, 'root': self.root})
        thechunk.generateBlocks(self)
        thechunk.generateVoxel()
        #thechunk.generateMarching()
        #place in loaded chunks dictionary
        print thechunk.getChunkID()
        self.chunks[thechunk.getChunkID()] = thechunk
        #place player
