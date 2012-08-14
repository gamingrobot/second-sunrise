#Planet
import sys
sys.path.insert(0, '..')
from MovableEntity import *
from PChunk import *
from panda3d.core import Vec3

from direct.stdpy import threading
from pandac.PandaModules import Thread
from direct.showbase.PythonUtil import Queue

from Util import MeshType

import random

from panda3d.core import PerlinNoise3
from panda3d.core import PerlinNoise2

_commandLineQueue = Queue()


class Planet(MovableEntity):
    """Planet"""
    def __init__(self, args):
        MovableEntity.__init__(self, args)
        self.x = args['x']
        self.y = args['y']
        self.z = args['z']
        self.root = args['root']
        self.planetNode = args['render'].attachNewNode("Planet_Gamma")
        self.meshtype = args['meshtype']
        self.planetNode.setPos(self.x, self.y, self.z)
        #init chunks
        self.chunkSize = 16
        self.chunks = {}
        self.psize = 16  # in chunks
        self.radius = self.chunkSize * (self.psize / 2)

        _thread = _ExecThread()
        _thread.start()
        scale = 100
        self.perlin = PerlinNoise3(scale, scale, 10)
        #self.perlin = PerlinNoise2(10, 10)

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
        spl = (1 * cs, 1 * cs, ((self.psize / 2) - 1) * cs)

        print spl
        self.playerchunk = self.genHash(spl[0], spl[1], spl[2])
        #generate chunk
        self.generateSpawnChunkBlocks(spl[0], spl[1], spl[2])
        self.generateSpawnChunkMesh(spl[0], spl[1], spl[2])
        self.generateChunks(spl[0], spl[1], spl[2])

        #place player
        playerspl = Vec3(spl[0] + 4, spl[1] + 4, spl[2] + self.chunkSize)
        player.setPos(playerspl)
        player.currentchunk = self.playerchunk

    def playerChangedChunk(self):
        print "Current Player Chunk " + self.playerchunk
        chunkcord = self.playerchunk.split(":")
        self.generateChunks(int(chunkcord[0]), int(chunkcord[1]), int(chunkcord[2]))
        #recalculate gravity
        #self.root.bulletworld.setGravity(Vec3(int(chunkcord[0]) * -1, int(chunkcord[1]) * -1, int(chunkcord[2]) * -1))

    def addChunk(self, x, y, z):
        nchunk = PChunk({'x': x, 'y': y, 'z': z,
            'planetNode': self.planetNode, 'root': self.root, 'planet': self, 'noise': self.perlin})
        _commandLineQueue.push({'command': 'blocks', 'chunk': nchunk})
        #nchunk.generateBlocks()
        #print nchunk.getChunkID()
        self.chunks[nchunk.getChunkID()] = nchunk

    def addNormChunk(self, x, y, z):
        nchunk = PChunk({'x': x, 'y': y, 'z': z,
            'planetNode': self.planetNode, 'root': self.root, 'planet': self, 'noise': self.perlin})
        #_commandLineQueue.push({'command': 'blocks', 'chunk': nchunk})
        nchunk.generateBlocks()
        #print nchunk.getChunkID()
        self.chunks[nchunk.getChunkID()] = nchunk

    def generateChunkMesh(self, x, y, z):
        """rand = random.randint(0, 1)
        if rand == 1:
            _commandLineQueue.push({'command': 'march', 'chunk': self.chunks[self.genHash(x, y, z)]})
        else:
            _commandLineQueue.push({'command': 'voxel', 'chunk': self.chunks[self.genHash(x, y, z)]})"""

        _commandLineQueue.push({'command': self.meshtype, 'chunk': self.chunks[self.genHash(x, y, z)]})

    def generateSpawnChunkMesh(self, x, y, z):
        if not self.chunks[self.genHash(x, y, z)].isEmpty():
            if not self.chunks[self.genHash(x, y, z)].meshGenerated():
                self.chunks[self.genHash(x, y, z)].generateMesh(self.meshtype)

    def generateSpawnChunkBlocks(self, x, y, z):
        #generate only positive chunks and check if they are already in the tree
        if not self.genHash(x, y, z) in self.chunks:
            self.addNormChunk(x, y, z)
        """#x y
        if not self.genHash(x + 16, y, z) in self.chunks:
            self.addNormChunk(x + 16, y, z)              # (x + 1, y, z)
        if not self.genHash(x + 16, y + 16, z) in self.chunks:
            self.addNormChunk(x + 16, y + 16, z)         # (x + 1, y + 1, z)
        if not self.genHash(x, y + 16, z) in self.chunks:
            self.addNormChunk(x, y + 16, z)              # (x, y + 1, z)
        #z
        if not self.genHash(x, y, z + 16) in self.chunks:
            self.addNormChunk(x, y, z + 16)                   # (x, y, z)
        if not self.genHash(x + 16, y, z + 16) in self.chunks:
            self.addNormChunk(x + 16, y, z + 16)              # (x + 1, y, z)
        if not self.genHash(x + 16, y + 16, z + 16) in self.chunks:
            self.addNormChunk(x + 16, y + 16, z + 16)         # (x + 1, y + 1, z)
        if not self.genHash(x, y + 16, z + 16) in self.chunks:
            self.addNormChunk(x, y + 16, z + 16)              # (x, y + 1, z)"""

    def generateChunkBlocks(self, x, y, z):
        #generate only positive chunks and check if they are already in the tree
        if not self.genHash(x, y, z) in self.chunks:
            self.addChunk(x, y, z)
        """#x y
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
            self.addChunk(x, y + 16, z + 16)              # (x, y + 1, z)"""

    def generateChunks(self, x, y, z):
        cs = self.chunkSize
        #generate blocks
        self.generateChunkBlocks(x, y, z)
        self.generateChunkMesh(x, y, z)
        #generate naboring chunks
        #x y
        self.generateChunkBlocks(x + cs, y, z)              # (x + 1, y, z)
        self.generateChunkMesh(x + cs, y, z)              # (x + 1, y, z)
        self.generateChunkBlocks(x + cs, y + cs, z)         # (x + 1, y + 1, z)
        self.generateChunkMesh(x + cs, y + cs, z)         # (x + 1, y + 1, z)
        self.generateChunkBlocks(x - cs, y + cs, z)         # (x + 1, y + 1, z)
        self.generateChunkMesh(x - cs, y + cs, z)         # (x + 1, y + 1, z)
        self.generateChunkBlocks(x - cs, y - cs, z)         # (x + 1, y + 1, z)
        self.generateChunkMesh(x - cs, y - cs, z)         # (x + 1, y + 1, z)
        self.generateChunkBlocks(x + cs, y - cs, z)         # (x + 1, y + 1, z)
        self.generateChunkMesh(x + cs, y - cs, z)         # (x + 1, y + 1, z)
        self.generateChunkBlocks(x, y + cs, z)              # (x, y + 1, z)
        self.generateChunkMesh(x, y + cs, z)              # (x, y + 1, z)
        self.generateChunkBlocks(x - cs, y, z)              # (x + 1, y, z)
        self.generateChunkMesh(x - cs, y, z)              # (x + 1, y, z)
        self.generateChunkBlocks(x, y - cs, z)              # (x, y + 1, z)
        self.generateChunkMesh(x, y - cs, z)              # (x, y + 1, z)

        # +z
        self.generateChunkBlocks(x, y, z + cs)                   # (x, y, z)
        self.generateChunkMesh(x, y, z + cs)                   # (x, y, z)
        self.generateChunkBlocks(x + cs, y, z + cs)              # (x + 1, y, z)
        self.generateChunkMesh(x + cs, y, z + cs)              # (x + 1, y, z)
        self.generateChunkBlocks(x + cs, y + cs, z + cs)         # (x + 1, y + 1, z)
        self.generateChunkMesh(x + cs, y + cs, z + cs)         # (x + 1, y + 1, z)
        self.generateChunkBlocks(x - cs, y + cs, z + cs)         # (x + 1, y + 1, z)
        self.generateChunkMesh(x - cs, y + cs, z + cs)         # (x + 1, y + 1, z)
        self.generateChunkBlocks(x - cs, y - cs, z + cs)         # (x + 1, y + 1, z)
        self.generateChunkMesh(x - cs, y - cs, z + cs)         # (x + 1, y + 1, z)
        self.generateChunkBlocks(x + cs, y - cs, z + cs)         # (x + 1, y + 1, z)
        self.generateChunkMesh(x + cs, y - cs, z + cs)         # (x + 1, y + 1, z)
        self.generateChunkBlocks(x, y + cs, z + cs)              # (x, y + 1, z)
        self.generateChunkMesh(x, y + cs, z + cs)              # (x, y + 1, z)
        self.generateChunkBlocks(x - cs, y, z + cs)              # (x + 1, y, z)
        self.generateChunkMesh(x - cs, y, z + cs)              # (x + 1, y, z)
        self.generateChunkBlocks(x, y - cs, z + cs)              # (x, y + 1, z)
        self.generateChunkMesh(x, y - cs, z + cs)              # (x, y + 1, z)

        # -z
        self.generateChunkBlocks(x, y, z - cs)              # (x, y, z)
        self.generateChunkMesh(x, y, z - cs)              # (x, y, z)
        self.generateChunkBlocks(x + cs, y, z - cs)              # (x + 1, y, z)
        self.generateChunkMesh(x + cs, y, z - cs)              # (x + 1, y, z)
        self.generateChunkBlocks(x + cs, y + cs, z - cs)         # (x + 1, y + 1, z)
        self.generateChunkMesh(x + cs, y + cs, z - cs)         # (x + 1, y + 1, z)
        self.generateChunkBlocks(x - cs, y + cs, z - cs)         # (x + 1, y + 1, z)
        self.generateChunkMesh(x - cs, y + cs, z - cs)         # (x + 1, y + 1, z)
        self.generateChunkBlocks(x - cs, y - cs, z - cs)         # (x + 1, y + 1, z)
        self.generateChunkMesh(x - cs, y - cs, z - cs)         # (x + 1, y + 1, z)
        self.generateChunkBlocks(x + cs, y - cs, z - cs)         # (x + 1, y + 1, z)
        self.generateChunkMesh(x + cs, y - cs, z - cs)         # (x + 1, y + 1, z)
        self.generateChunkBlocks(x, y + cs, z - cs)              # (x, y + 1, z)
        self.generateChunkMesh(x, y + cs, z - cs)              # (x, y + 1, z)
        self.generateChunkBlocks(x - cs, y, z - cs)              # (x + 1, y, z)
        self.generateChunkMesh(x - cs, y, z - cs)              # (x + 1, y, z)
        self.generateChunkBlocks(x, y - cs, z - cs)              # (x, y + 1, z)
        self.generateChunkMesh(x, y - cs, z - cs)              # (x, y + 1, z)

    def genHash(self, x, y, z):
        return str(x) + ":" + str(y) + ":" + str(z)

    def removeBlock(self, chunkid, x, y, z):
        self.chunks[chunkid].removeBlock(x, y, z)
        t = threading.Thread(target=self.chunks[chunkid].generateMesh, args=(self.meshtype,))
        t.start()

    def placeBlock(self, chunkid, x, y, z):
        self.chunks[chunkid].placeBlock(x, y, z)
        t = threading.Thread(target=self.chunks[chunkid].generateMesh, args=(self.meshtype,))
        t.start()

    def testBox(self, x, y, z):
        model = self.root.loader.loadModel('models/box.egg')
        model.reparentTo(self.planetNode)
        model.setPos(x, y, z)


class _ExecThread(threading.Thread):
    def run(self):
        while True:
            while not _commandLineQueue.isEmpty():
                popque = _commandLineQueue.pop()
                #print _commandLineQueue.top()
                chunk = popque['chunk']
                if popque['command'] == 'blocks':
                    chunk.generateBlocks()
                if popque['command'] == MeshType.MarchingCubes:
                    #if not chunk.isEmpty():
                    if not chunk.meshGenerated():
                        chunk.generateMesh(MeshType.MarchingCubes)
                if popque['command'] == MeshType.SurfaceNet:
                    #if not chunk.isEmpty():
                    if not chunk.meshGenerated():
                        chunk.generateMesh(MeshType.SurfaceNet)
                if popque['command'] == MeshType.Voxel:
                    #if not chunk.isEmpty():
                    #    if not chunk.meshGenerated():
                    chunk.generateMesh(MeshType.Voxel)
                Thread.sleep(0.04)
            Thread.sleep(0.04)
