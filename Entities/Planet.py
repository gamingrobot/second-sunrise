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
        self.size = 1
        #self.planetNode = sm.getRootSceneNode().createChildSceneNode("planet" + args['name'], ogre.Vector3(self.x, self.y, self.z))

        self.numChunks = 0
        self.numChunks += 1
        self.aChunk = Chunk({'x': 0, 'y': 0, 'z': 0, 'planetNode': self.planetNode, 'senemanager': args['senemanager'], 'name': str(self.numChunks)})
        #chunks
        #self.chunks = []
        #for x in range(0, args['maxc']):
        #    s = Chunk()
        #    self.chunks.append(s)

    def __str__(self):
        return "A Planet"
