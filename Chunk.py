#Chunk.py
import numpy
import BlockManager


class Chunk:
    """Chunk contains 32x32x32 blocks"""
    def __init__(self, args):
        self.x = args['x']
        self.y = args['y']
        self.z = args['z']
        self.size = 8
        self.blocks = numpy.zeros((self.size, self.size, self.size), dtype=numpy.object)
        self.blockSize = 10
        #pn = args['planetNode']
        self.chunkNode = None
        #self.chunkNode = pn.createChildSceneNode("chunk" + args['name'], ogre.Vector3(self.x, self.y, self.z))
        #self.chunkNode = ogre.StaticGeometry(args['senemanager'], "Boxes")
        #pGeom.setRegionDemensions(ogre.Vector3(8 * 10, 8 * 10, 8 * 10))
        #BlockManager.Space({'x': 0, 'y': 0, 'z': 0, 'chunkNode': None, 'senemanager': args['senemanager'], 'name': '000'})
        it = numpy.nditer(self.blocks, op_flags=['readwrite'], flags=['multi_index', 'refs_ok'])
        while not it.finished:
            index = it.multi_index
            #it[0] = BlockManager.Space({'x': index[0]*self.blockSize, 'y': index[1]*self.blockSize, 'z': index[2]*self.blockSize, 'chunkNode': self.chunkNode, 'senemanager': args['senemanager'], 'name': '000'})
            it.iternext()
