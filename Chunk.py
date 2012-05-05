#Chunk.py
from panda3d.core import GeomVertexFormat
from panda3d.core import GeomVertexData
from panda3d.core import GeomVertexWriter
from panda3d.core import GeomTriangles
from panda3d.core import GeomNode
from panda3d.core import Geom
import numpy as np
import random
import BlockManager


class Chunk:
    """Chunk contains 32x32x32 blocks"""
    def __init__(self, args):
        self.x = args['x']
        self.y = args['y']
        self.z = args['z']
        self.size = 8
        self.blocks = np.zeros((self.size, self.size, self.size), dtype=np.object)
        self.blockSize = 1
        #init numpy
        it = np.nditer(self.blocks, op_flags=['readwrite'], flags=['multi_index', 'refs_ok'])
        while not it.finished:
            index = it.multi_index
            arandom = random.randint(0, 1)
            #arandom = 1
            if arandom == 1:
                it[0] = BlockManager.Dirt(
                    {'x': index[0] * self.blockSize, 'y': index[1] * self.blockSize, 'z': index[2] * self.blockSize, 'name': '000'})
            else:
                it[0] = BlockManager.Air(
                    {'x': index[0] * self.blockSize, 'y': index[1] * self.blockSize, 'z': index[2] * self.blockSize, 'name': '000'})
            it.iternext()

        #render a cube
        format = GeomVertexFormat.registerFormat(GeomVertexFormat.getV3n3c4t2())
        vdata = GeomVertexData('chunk', format, Geom.UHStatic)

        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color = GeomVertexWriter(vdata, 'color')
        texcoord = GeomVertexWriter(vdata, 'texcoord')

        prim = GeomTriangles(Geom.UHStatic)
        self.vertexcount = 0

        for x in xrange(0, self.size):
            for y in xrange(0, self.size):
                for z in xrange(0, self.size):
                    block = self.blocks[x, y, z]
                    #current block exists
                    if not self.isEmptyBlock(block):
                        #Not air or space block render
                        #left
                        block = None
                        if x >= 1:
                            block = self.blocks[x - 1, y, z]
                        if(self.isEmptyBlock(block)):
                            #render that side
                            #print "Render Left Side" + str(x) + "," + str(y) + "," + str(z)
                            shade = 0.45
                            #line corners
                            #0
                            vertex.addData3f(x, y, z)
                            normal.addData3f(0, 0, 1)
                            color.addData4f(shade, shade, shade, 1)
                            texcoord.addData2f(0, 0)
                            #1
                            vertex.addData3f(x, y + 1, z + 1)
                            normal.addData3f(0, 0, 1)
                            color.addData4f(shade, shade, shade, 1)
                            texcoord.addData2f(0, 1)
                            #edge corners
                            #2
                            vertex.addData3f(x, y, z + 1)
                            normal.addData3f(0, 0, 1)
                            color.addData4f(shade, shade, shade, 1)
                            texcoord.addData2f(0, 0)
                            #3
                            vertex.addData3f(x, y + 1, z)
                            normal.addData3f(0, 0, 1)
                            color.addData4f(shade, shade, shade, 1)
                            texcoord.addData2f(0, 1)
                            #draw triangles
                            prim.addVertices(self.vertexcount, self.vertexcount + 2, self.vertexcount + 1)
                            prim.addVertices(self.vertexcount + 1, self.vertexcount + 3, self.vertexcount)
                            #increment vertexcount
                            self.vertexcount += 4
                        #front
                        block = None
                        if y >= 1:
                            block = self.blocks[x, y - 1, z]
                        if(self.isEmptyBlock(block)):
                            #render that side
                            #print "Render Front Side" + str(x) + "," + str(y) + "," + str(z)
                            shade = 0.1
                            #line corners
                            #0
                            vertex.addData3f(x + 1, y, z)
                            normal.addData3f(0, 0, 1)
                            color.addData4f(shade, shade, shade, 1)
                            texcoord.addData2f(1, 0)
                            #1
                            vertex.addData3f(x, y, z + 1)
                            normal.addData3f(0, 0, 1)
                            color.addData4f(shade, shade, shade, 1)
                            texcoord.addData2f(0, 0)
                            #edge corners
                            #2
                            vertex.addData3f(x + 1, y, z + 1)
                            normal.addData3f(0, 0, 1)
                            color.addData4f(shade, shade, shade, 1)
                            texcoord.addData2f(1, 0)
                            #3
                            vertex.addData3f(x, y, z)
                            normal.addData3f(0, 0, 1)
                            color.addData4f(shade, shade, shade, 1)
                            texcoord.addData2f(0, 0)
                            #draw triangles
                            prim.addVertices(self.vertexcount, self.vertexcount + 2, self.vertexcount + 1)
                            prim.addVertices(self.vertexcount + 1, self.vertexcount + 3, self.vertexcount)
                            #increment vertexcount
                            self.vertexcount += 4

                        #right
                        block = None
                        if x < self.size - 1:
                            block = self.blocks[x + 1, y, z]
                        if(self.isEmptyBlock(block)):
                            #render that side
                            #print "Render Right Side" + str(x) + "," + str(y) + "," + str(z)
                            shade = 0.7
                            #line corners
                            #0
                            vertex.addData3f(x + 1, y + 1, z + 1)
                            normal.addData3f(0, 0, 1)
                            color.addData4f(shade, shade, shade, 1)
                            texcoord.addData2f(1, 1)
                            #1
                            vertex.addData3f(x + 1, y, z)
                            normal.addData3f(0, 0, 1)
                            color.addData4f(shade, shade, shade, 1)
                            texcoord.addData2f(1, 0)
                            #edge corners
                            #2
                            vertex.addData3f(x + 1, y, z + 1)
                            normal.addData3f(0, 0, 1)
                            color.addData4f(shade, shade, shade, 1)
                            texcoord.addData2f(1, 0)
                            #3
                            vertex.addData3f(x + 1, y + 1, z)
                            normal.addData3f(0, 0, 1)
                            color.addData4f(shade, shade, shade, 1)
                            texcoord.addData2f(1, 1)
                            #draw triangles
                            prim.addVertices(self.vertexcount, self.vertexcount + 2, self.vertexcount + 1)
                            prim.addVertices(self.vertexcount + 1, self.vertexcount + 3, self.vertexcount)
                            #increment vertexcount
                            self.vertexcount += 4

                        #back
                        block = None
                        if y < self.size - 1:
                            block = self.blocks[x, y + 1, z]
                        if(self.isEmptyBlock(block)):
                            #render that side
                            #print "Render Back Side" + str(x) + "," + str(y) + "," + str(z)
                            shade = 0.5
                            #line corners
                            #0
                            vertex.addData3f(x, y + 1, z + 1)
                            normal.addData3f(0, 0, 1)
                            color.addData4f(shade, shade, shade, 1)
                            texcoord.addData2f(0, 1)
                            #1
                            vertex.addData3f(x + 1, y + 1, z)
                            normal.addData3f(0, 0, 1)
                            color.addData4f(shade, shade, shade, 1)
                            texcoord.addData2f(1, 1)
                            #edge corners
                            #2
                            vertex.addData3f(x + 1, y + 1, z + 1)
                            normal.addData3f(0, 0, 1)
                            color.addData4f(shade, shade, shade, 1)
                            texcoord.addData2f(1, 1)
                            #3
                            vertex.addData3f(x, y + 1, z)
                            normal.addData3f(0, 0, 1)
                            color.addData4f(shade, shade, shade, 1)
                            texcoord.addData2f(0, 1)
                            #draw triangles
                            prim.addVertices(self.vertexcount, self.vertexcount + 2, self.vertexcount + 1)
                            prim.addVertices(self.vertexcount + 1, self.vertexcount + 3, self.vertexcount)
                            #increment vertexcount
                            self.vertexcount += 4

                        #bottom
                        block = None
                        if z > 1:
                            block = self.blocks[x, y, z - 1]
                        if(self.isEmptyBlock(block)):
                            #render that side
                            #print "Render Bottom Side" + str(x) + "," + str(y) + "," + str(z)
                            shade = 0.3
                            #line corners
                            #0
                            vertex.addData3f(x, y + 1, z)
                            normal.addData3f(0, 0, 1)
                            color.addData4f(shade, shade, shade, 1)
                            texcoord.addData2f(0, 1)
                            #1
                            vertex.addData3f(x + 1, y, z)
                            normal.addData3f(0, 0, 1)
                            color.addData4f(shade, shade, shade, 1)
                            texcoord.addData2f(1, 0)
                            #edge corners
                            #2
                            vertex.addData3f(x + 1, y + 1, z)
                            normal.addData3f(0, 0, 1)
                            color.addData4f(shade, shade, shade, 1)
                            texcoord.addData2f(1, 1)
                            #3
                            vertex.addData3f(x, y, z)
                            normal.addData3f(0, 0, 1)
                            color.addData4f(shade, shade, shade, 1)
                            texcoord.addData2f(0, 0)
                            #draw triangles
                            prim.addVertices(self.vertexcount, self.vertexcount + 2, self.vertexcount + 1)
                            prim.addVertices(self.vertexcount + 1, self.vertexcount + 3, self.vertexcount)
                            #increment vertexcount
                            self.vertexcount += 4

                        #top
                        block = None
                        if z < self.size - 1:
                            block = self.blocks[x, y, z + 1]
                        if(self.isEmptyBlock(block)):
                            #render that side
                            #print "Render Top Side" + str(x) + "," + str(y) + "," + str(z)
                            shade = 0.9
                            #line corners
                            #0
                            vertex.addData3f(x + 1, y, z + 1)
                            normal.addData3f(0, 0, 1)
                            color.addData4f(shade, shade, shade, 1)
                            texcoord.addData2f(1, 0)
                            #1
                            vertex.addData3f(x, y + 1, z + 1)
                            normal.addData3f(0, 0, 1)
                            color.addData4f(shade, shade, shade, 1)
                            texcoord.addData2f(0, 1)
                            #edge corners
                            #2
                            vertex.addData3f(x + 1, y + 1, z + 1)
                            normal.addData3f(0, 0, 1)
                            color.addData4f(shade, shade, shade, 1)
                            texcoord.addData2f(1, 1)
                            #3
                            vertex.addData3f(x, y, z + 1)
                            normal.addData3f(0, 0, 1)
                            color.addData4f(shade, shade, shade, 1)
                            texcoord.addData2f(0, 0)
                            #draw triangles
                            prim.addVertices(self.vertexcount, self.vertexcount + 2, self.vertexcount + 1)
                            prim.addVertices(self.vertexcount + 1, self.vertexcount + 3, self.vertexcount)
                            #increment vertexcount
                            self.vertexcount += 4

        #attach primitives and render
        geom = Geom(vdata)
        geom.addPrimitive(prim)

        node = GeomNode('gnode')
        node.addGeom(geom)

        self.node = args['planetNode'].attachNewNode(node)
        self.node.setPos(self.x + self.size, self.y + self.size, self.z + self.size)

        #store data in chunk class so dont have to regenerate

    def isEmptyBlock(self, block):
        if block == None:
            return True
        elif block.__class__.__name__ != "Air" and block.__class__.__name__ != "Space":
            return False
        else:
            return True
