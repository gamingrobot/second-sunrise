#Chunk.py
from panda3d.core import GeomVertexFormat
from panda3d.core import GeomVertexData
from panda3d.core import GeomVertexWriter
from panda3d.core import GeomTriangles
from panda3d.core import GeomNode
from panda3d.core import Geom
from panda3d.core import Point3
from panda3d.core import VBase3
from panda3d.core import BitMask32
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape

import numpy as np
import math
from Blocks import *


class PChunk:
    """Chunk contains 16x16x16 blocks"""
    def __init__(self, args):
        self.x = args['x']
        self.y = args['y']
        self.z = args['z']
        self.id = str(self.x) + ":" + str(self.y) + ":" + str(self.z)
        self.planetNode = args['planetNode']
        self.root = args['root']
        self.planet = args['planet']
        self.empty = True
        self.meshed = False
        self.level = float(0.0)

    def getChunkID(self):
        return self.id

    def generateBlocks(self):
        #make a nicer name for math.fabs()
        ab = math.fabs

        self.size = self.planet.chunkSize
        self.numchunks = self.planet.psize
        self.radius = self.planet.radius  # in blocks
        self.blocks = np.zeros((self.size, self.size, self.size), dtype=np.object)
        self.blockSize = 1
        #init numpy
        it = np.nditer(self.blocks, op_flags=['readwrite'], flags=['multi_index', 'refs_ok'])
        while not it.finished:
            index = it.multi_index
            #arandom = random.randint(0, 1)
            #arandom = 1
            if math.sqrt((ab(self.x + index[0])) ** 2 + (ab(self.y + index[1])) ** 2 + (ab(self.z + index[2])) ** 2) <= self.radius:
                self.empty = False
                it[0] = Dirt(
                    {'x': index[0], 'y': index[1], 'z': index[2], 'density': float(1.0), 'name': '000'})
            else:
                it[0] = Air(
                    {'x': index[0], 'y': index[1], 'z': index[2], 'density': float(-1.0), 'name': '000'})
            it.iternext()

    def removeBlock(self, x, y, z, voxel=False):
        print "removing" + str(x) + "," + str(y) + "," + str(z)
        print self.blocks[x][y][z]
        self.blocks[x][y][z] = Air(
                    {'x': x, 'y': y, 'z': z, 'density': float(-1.0), 'name': '000'})

    def placeBlock(self, x, y, z, voxel=False):
        print "placing" + str(x) + "," + str(y) + "," + str(z)
        print self.blocks[x][y][z]
        self.blocks[x][y][z] = Dirt(
                    {'x': x, 'y': y, 'z': z, 'density': float(1.0), 'name': '000'})

    def isEmpty(self):
        return self.empty

    def meshGenerated(self):
        return self.meshed

    def generateMesh(self, voxel=False):
        self.chunks = self.planet.chunks
        if not voxel:
            triangles = self.generateMarchingMesh()
        else:
            triangles = self.generateVoxelMesh()

        format = GeomVertexFormat.registerFormat(GeomVertexFormat.getV3n3c4t2())
        vdata = GeomVertexData('chunk', format, Geom.UHStatic)

        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color = GeomVertexWriter(vdata, 'color')
        texcoord = GeomVertexWriter(vdata, 'texcoord')
        prim = GeomTriangles(Geom.UHStatic)

        self.vertexcount = 0
        for triangle in triangles:
            for avertex in triangle:
                #print triangle
                #make vertices here
                shade = 0.5
                vertex.addData3f(avertex[0], avertex[1], avertex[2])
                #fix normals
                x1, y1, z1 = triangle[0][0], triangle[0][1], triangle[0][2]
                x2, y2, z2 = triangle[1][0], triangle[1][1], triangle[1][2]
                x3, y3, z3 = triangle[2][0], triangle[2][1], triangle[2][2]
                normx = (z1 - z2) * (y3 - y2) - (y1 - y2) * (z3 - z2)
                normy = (x1 - x2) * (z3 - z2) - (z1 - z2) * (x3 - x2)
                normz = (y1 - y2) * (x3 - x2) - (x1 - x2) * (y3 - y2)
                normlength = math.sqrt(normx ** 2 + normy ** 2 + normz ** 2)
                normx /= normlength
                normy /= normlength
                normz /= normlength

                normal.addData3f(normx, normy, normz)
                color.addData4f(shade, shade, shade, 1)
                texcoord.addData2f(1, 0)

            #make triangles
            prim.addVertices(self.vertexcount, self.vertexcount + 1, self.vertexcount + 2)
            self.vertexcount += 3

        prim.closePrimitive()
        #print prim
        #attach primitives and render
        geom = Geom(vdata)
        geom.addPrimitive(prim)

        try:
            self.node.removeNode()
            self.bulletnode.removeShape(self.bulletshape)
            self.root.bulletworld.removeRigidBody(self.bulletnode)
            self.bulletnp.removeNode()
        except AttributeError:
            pass

        node = GeomNode(self.id)
        node.addGeom(geom)
        self.node = self.planetNode.attachNewNode(node)
        if not voxel:
            self.node.setPos(self.x, self.y, self.z - 0.5)
        else:
            self.node.setPos(self.x, self.y, self.z)
        self.node.setTag('Pickable', '1')
        self.meshed = True

        #do bullet meshing
        #if self.id == self.planet.playerchunk:
        mesh = BulletTriangleMesh()
        for triangle in triangles:
            p0 = Point3(triangle[0][0], triangle[0][1], triangle[0][2])
            p1 = Point3(triangle[1][0], triangle[1][1], triangle[1][2])
            p2 = Point3(triangle[2][0], triangle[2][1], triangle[2][2])
            mesh.addTriangle(p0, p1, p2)

        self.bulletshape = BulletTriangleMeshShape(mesh, dynamic=False)
        self.bulletnode = BulletRigidBodyNode(self.id)
        self.bulletnode.addShape(self.bulletshape)
        #self.bulletnode.setDeactivationEnabled(False)
        #self.bulletnode.setAnisotropicFriction(VBase3(10, 10, 0))
        self.bulletnp = self.planetNode.attachNewNode(self.bulletnode)
        if not voxel:
            self.bulletnp.setPos(self.x, self.y, self.z - 0.5)
        else:
            self.bulletnp.setPos(self.x, self.y, self.z)
        self.bulletnp.setCollideMask(BitMask32.allOn())
        self.root.bulletworld.attachRigidBody(self.bulletnode)

    def generateMarchingMesh(self):
        draw = Iso(self, self.size, self.chunks)
        triangles = draw.grid()
        return triangles

    def generateVoxelMesh(self):
        triangles = []
        for x in xrange(0, self.size):
            for y in xrange(0, self.size):
                for z in xrange(0, self.size):
                    block = self.blocks[x, y, z]
                    #current block exists
                    if not self.isEmptyBlock(block):
                        #left
                        block = None
                        if x >= 1:
                            block = self.blocks[x - 1, y, z]
                        if self.isEmptyBlock(block):
                            #triangles.append([[], [], []])
                            triangles.append([[x, y, z], [x, y, z + 1], [x, y + 1, z + 1]])
                            triangles.append([[x, y + 1, z + 1], [x, y + 1, z], [x, y, z]])
                        #front
                        block = None
                        if y >= 1:
                            block = self.blocks[x, y - 1, z]
                        if self.isEmptyBlock(block):
                            triangles.append([[x + 1, y, z], [x + 1, y, z + 1], [x, y, z + 1]])
                            triangles.append([[x, y, z + 1], [x, y, z], [x + 1, y, z]])
                        #right
                        block = None
                        if x < self.size - 1:
                            block = self.blocks[x + 1, y, z]
                        if self.isEmptyBlock(block):
                            triangles.append([[x + 1, y + 1, z + 1], [x + 1, y, z + 1], [x + 1, y, z]])
                            triangles.append([[x + 1, y, z], [x + 1, y + 1, z], [x + 1, y + 1, z + 1]])
                        #back
                        block = None
                        if y < self.size - 1:
                            block = self.blocks[x, y + 1, z]
                        if self.isEmptyBlock(block):
                            triangles.append([[x, y + 1, z + 1], [x + 1, y + 1, z + 1], [x + 1, y + 1, z]])
                            triangles.append([[x + 1, y + 1, z], [x, y + 1, z], [x, y + 1, z + 1]])
                        #bottom
                        block = None
                        if z > 1:
                            block = self.blocks[x, y, z - 1]
                        if self.isEmptyBlock(block):
                            triangles.append([[x, y + 1, z], [x + 1, y + 1, z], [x + 1, y, z]])
                            triangles.append([[x + 1, y, z], [x, y, z], [x, y + 1, z]])
                        #top
                        block = None
                        if z < self.size - 1:
                            block = self.blocks[x, y, z + 1]
                        if self.isEmptyBlock(block):
                            triangles.append([[x + 1, y, z + 1], [x + 1, y + 1, z + 1], [x, y + 1, z + 1]])
                            triangles.append([[x, y + 1, z + 1], [x, y, z + 1], [x + 1, y, z + 1]])
        return triangles

    def isEmptyBlock(self, block):
        if block == None:
            return True
        elif block.__class__.__name__ != "Air" and block.__class__.__name__ != "Space":
            return False
        else:
            return True

    def genHash(self, x, y, z):
        return str(x) + ":" + str(y) + ":" + str(z)


class Iso:

    class GridCell:
        def __init__(self):
            self.position = [(0.0, 0.0, 0.0) for i in range(8)]
            self.value = None

    def __init__(self, chunk, size, chunks):
        self.blocks = chunk.blocks
        self.x = chunk.x
        self.y = chunk.y
        self.z = chunk.z
        self.size = size
        self.level = float(0.0)
        self.triangles = []
        self.chunks = chunks

    def vertexInterp(self, p1, p2, valp1, valp2):
        if abs(self.level - valp1) < 0.000000000001:
            return p1
        if abs(self.level - valp2) < 0.000000000001:
            return p2
        if abs(valp1 - valp2) < 0.0000000001:
            return p1
        mu = (self.level - valp1) / (valp2 - valp1)
        p = (p1[0] + mu * (p2[0] - p1[0]),
             p1[1] + mu * (p2[1] - p1[1]),
             p1[2] + mu * (p2[2] - p1[2]))
        return p

    def cube(self, cell):
        cubeIndex = 0
        value = cell.value
        position = cell.position
        level = self.level

        vertexList = [[0.0, 0.0, 0.0] for i in range(12)]
        if value[0] < level:
            cubeIndex |= 1
        if value[1] < level:
            cubeIndex |= 2
        if value[2] < level:
            cubeIndex |= 4
        if value[3] < level:
            cubeIndex |= 8
        if value[4] < level:
            cubeIndex |= 16
        if value[5] < level:
            cubeIndex |= 32
        if value[6] < level:
            cubeIndex |= 64
        if value[7] < level:
            cubeIndex |= 128

        et = edgeTable[cubeIndex]
        vi = self.vertexInterp

        if et == 0:
            return 0
        if et & 1:
            vertexList[0] = vi(position[0], position[1], value[0], value[1])
        if et & 2:
            vertexList[1] = vi(position[1], position[2], value[1], value[2])
        if et & 4:
            vertexList[2] = vi(position[2], position[3], value[2], value[3])
        if et & 8:
            vertexList[3] = vi(position[3], position[0], value[3], value[0])
        if et & 16:
            vertexList[4] = vi(position[4], position[5], value[4], value[5])
        if et & 32:
            vertexList[5] = vi(position[5], position[6], value[5], value[6])
        if et & 64:
            vertexList[6] = vi(position[6], position[7], value[6], value[7])
        if et & 128:
            vertexList[7] = vi(position[7], position[4], value[7], value[4])
        if et & 256:
            vertexList[8] = vi(position[0], position[4], value[0], value[4])
        if et & 512:
            vertexList[9] = vi(position[1], position[5], value[1], value[5])
        if et & 1024:
            vertexList[10] = vi(position[2], position[6], value[2], value[6])
        if et & 2048:
            vertexList[11] = vi(position[3], position[7], value[3], value[7])

        ntriangle = 0
        tt = triTable[cubeIndex]
        for i in range(0, 16, 3):
            #Thread.forceYield()
            if tt[i] != -1:
                self.triangles.append((vertexList[tt[i]],
                                       vertexList[tt[i + 1]],
                                       vertexList[tt[i + 2]]))
                ntriangle += 1
        return ntriangle

    def grid(self):
        #triangles = []
        for x in xrange(0, self.size):
            for y in xrange(0, self.size):
                for z in xrange(0, self.size):
                    #Thread.forceYield()
                    #block = self.blocks[x, y, z]
                    p = self.GridCell()
                    position = p.position
                    #(x, y, z) = (float(i), float(j), float(k))
                    position[0] = (x, y, z)
                    position[1] = (x + 1, y, z)
                    position[2] = (x + 1, y + 1, z)
                    position[3] = (x, y + 1, z)
                    position[4] = (x, y, z + 1)
                    position[5] = (x + 1, y, z + 1)
                    position[6] = (x + 1, y + 1, z + 1)
                    position[7] = (x, y + 1, z + 1)

                    #print self.genHash(x,y,z)
                    if x == self.size - 1 and y == self.size - 1 and z == self.size - 1:
                        #print "in if 1" + self.genHash(x, y, z)
                        p.value = (self.blocks[x, y, z].getDensity(),
                                self.chunks[self.genHash(self.x + 16, self.y, self.z)].blocks[0, 15, 15].getDensity(),
                                self.chunks[self.genHash(self.x + 16, self.y + 16, self.z)].blocks[0, 0, 15].getDensity(),
                                self.chunks[self.genHash(self.x, self.y + 16, self.z)].blocks[15, 0, 15].getDensity(),
                                self.chunks[self.genHash(self.x, self.y, self.z + 16)].blocks[15, 15, 0].getDensity(),
                                self.chunks[self.genHash(self.x + 16, self.y, self.z + 16)].blocks[0, 15, 0].getDensity(),
                                self.chunks[self.genHash(self.x + 16, self.y + 16, self.z + 16)].blocks[0, 0, 0].getDensity(),
                                self.chunks[self.genHash(self.x, self.y + 16, self.z + 16)].blocks[15, 0, 0].getDensity())

                    elif x == self.size - 1 and y == self.size - 1:
                        #print "in if 2" + self.genHash(x, y, z)
                        p.value = (self.blocks[x, y, z].getDensity(),
                                self.chunks[self.genHash(self.x + 16, self.y, self.z)].blocks[0, 15, z].getDensity(),
                                self.chunks[self.genHash(self.x + 16, self.y + 16, self.z)].blocks[0, 0, z].getDensity(),  # watch out here might cause problem
                                self.chunks[self.genHash(self.x, self.y + 16, self.z)].blocks[15, 0, z].getDensity(),
                                self.blocks[x, y, z + 1].getDensity(),
                                self.chunks[self.genHash(self.x + 16, self.y, self.z)].blocks[0, 15, z + 1].getDensity(),
                                self.chunks[self.genHash(self.x + 16, self.y + 16, self.z)].blocks[0, 0, z + 1].getDensity(),
                                self.chunks[self.genHash(self.x, self.y + 16, self.z)].blocks[15, 0, z + 1].getDensity())

                    elif x == self.size - 1 and z == self.size - 1:
                        #print "in if 3 " + self.genHash(x, y, z)
                        p.value = (self.blocks[x, y, z].getDensity(),
                                self.chunks[self.genHash(self.x + 16, self.y, self.z)].blocks[0, y, 15].getDensity(),
                                self.chunks[self.genHash(self.x + 16, self.y, self.z)].blocks[0, y + 1, 15].getDensity(),
                                self.blocks[x, y + 1, z].getDensity(),
                                self.chunks[self.genHash(self.x, self.y, self.z + 16)].blocks[15, y, 0].getDensity(),
                                self.chunks[self.genHash(self.x + 16, self.y, self.z + 16)].blocks[0, y, 0].getDensity(),  # watch out here might cause problem
                                self.chunks[self.genHash(self.x + 16, self.y, self.z + 16)].blocks[0, y + 1, 0].getDensity(),
                                self.chunks[self.genHash(self.x, self.y, self.z + 16)].blocks[15, y + 1, 0].getDensity())

                    elif y == self.size - 1 and z == self.size - 1:
                        #print "in if 4" + self.genHash(x, y, z)
                        p.value = (self.blocks[x, y, z].getDensity(),
                                self.blocks[x + 1, y, z].getDensity(),
                                self.chunks[self.genHash(self.x, self.y + 16, self.z)].blocks[x + 1, 0, 15].getDensity(),
                                self.chunks[self.genHash(self.x, self.y + 16, self.z)].blocks[x, 0, 15].getDensity(),
                                self.chunks[self.genHash(self.x, self.y, self.z + 16)].blocks[x, 15, 0].getDensity(),
                                self.chunks[self.genHash(self.x, self.y, self.z + 16)].blocks[x + 1, 15, 0].getDensity(),
                                self.chunks[self.genHash(self.x, self.y + 16, self.z + 16)].blocks[x + 1, 0, 0].getDensity(),
                                self.chunks[self.genHash(self.x, self.y + 16, self.z + 16)].blocks[x, 0, 0].getDensity())  # watch out here might cause problem

                    elif x == self.size - 1:
                        #print "in if 5" + self.genHash(x, y, z)
                        p.value = (self.blocks[x, y, z].getDensity(),
                                self.chunks[self.genHash(self.x + 16, self.y, self.z)].blocks[0, y, z].getDensity(),
                                self.chunks[self.genHash(self.x + 16, self.y, self.z)].blocks[0, y + 1, z].getDensity(),
                                self.blocks[x, y + 1, z].getDensity(),
                                self.blocks[x, y, z + 1].getDensity(),
                                self.chunks[self.genHash(self.x + 16, self.y, self.z)].blocks[0, y, z + 1].getDensity(),
                                self.chunks[self.genHash(self.x + 16, self.y, self.z)].blocks[0, y + 1, z + 1].getDensity(),
                                self.blocks[x, y + 1, z + 1].getDensity())

                    elif y == self.size - 1:
                        #print "in if 6" + self.genHash(x, y, z)
                        p.value = (self.blocks[x, y, z].getDensity(),
                                self.blocks[x + 1, y, z].getDensity(),
                                self.chunks[self.genHash(self.x, self.y + 16, self.z)].blocks[x + 1, 0, z].getDensity(),
                                self.chunks[self.genHash(self.x, self.y + 16, self.z)].blocks[x, 0, z].getDensity(),
                                self.blocks[x, y, z + 1].getDensity(),
                                self.blocks[x + 1, y, z + 1].getDensity(),
                                self.chunks[self.genHash(self.x, self.y + 16, self.z)].blocks[x + 1, 0, z + 1].getDensity(),
                                self.chunks[self.genHash(self.x, self.y + 16, self.z)].blocks[x, 0, z + 1].getDensity())

                    elif z == self.size - 1:
                        #print "in if 7" + self.genHash(x, y, z)
                        p.value = (self.blocks[x, y, z].getDensity(),
                                self.blocks[x + 1, y, z].getDensity(),
                                self.blocks[x + 1, y + 1, z].getDensity(),
                                self.blocks[x, y + 1, z].getDensity(),
                                self.chunks[self.genHash(self.x, self.y, self.z + 16)].blocks[x, y, 0].getDensity(),
                                self.chunks[self.genHash(self.x, self.y, self.z + 16)].blocks[x + 1, y, 0].getDensity(),
                                self.chunks[self.genHash(self.x, self.y, self.z + 16)].blocks[x + 1, y + 1, 0].getDensity(),
                                self.chunks[self.genHash(self.x, self.y, self.z + 16)].blocks[x, y + 1, 0].getDensity())

                    else:
                        #print "in else" + self.genHash(x, y, z)
                        p.value = (self.blocks[x, y, z].getDensity(),
                                self.blocks[x + 1, y, z].getDensity(),
                                self.blocks[x + 1, y + 1, z].getDensity(),
                                self.blocks[x, y + 1, z].getDensity(),
                                self.blocks[x, y, z + 1].getDensity(),
                                self.blocks[x + 1, y, z + 1].getDensity(),
                                self.blocks[x + 1, y + 1, z + 1].getDensity(),
                                self.blocks[x, y + 1, z + 1].getDensity())
                    self.cube(p)
        return self.triangles

    def genHash(self, x, y, z):
        return str(x) + ":" + str(y) + ":" + str(z)

edgeTable = [0x0, 0x109, 0x203, 0x30a, 0x406, 0x50f, 0x605, 0x70c,
0x80c, 0x905, 0xa0f, 0xb06, 0xc0a, 0xd03, 0xe09, 0xf00,
0x190, 0x99 , 0x393, 0x29a, 0x596, 0x49f, 0x795, 0x69c,
0x99c, 0x895, 0xb9f, 0xa96, 0xd9a, 0xc93, 0xf99, 0xe90,
0x230, 0x339, 0x33 , 0x13a, 0x636, 0x73f, 0x435, 0x53c,
0xa3c, 0xb35, 0x83f, 0x936, 0xe3a, 0xf33, 0xc39, 0xd30,
0x3a0, 0x2a9, 0x1a3, 0xaa , 0x7a6, 0x6af, 0x5a5, 0x4ac,
0xbac, 0xaa5, 0x9af, 0x8a6, 0xfaa, 0xea3, 0xda9, 0xca0,
0x460, 0x569, 0x663, 0x76a, 0x66 , 0x16f, 0x265, 0x36c,
0xc6c, 0xd65, 0xe6f, 0xf66, 0x86a, 0x963, 0xa69, 0xb60,
0x5f0, 0x4f9, 0x7f3, 0x6fa, 0x1f6, 0xff , 0x3f5, 0x2fc,
0xdfc, 0xcf5, 0xfff, 0xef6, 0x9fa, 0x8f3, 0xbf9, 0xaf0,
0x650, 0x759, 0x453, 0x55a, 0x256, 0x35f, 0x55 , 0x15c,
0xe5c, 0xf55, 0xc5f, 0xd56, 0xa5a, 0xb53, 0x859, 0x950,
0x7c0, 0x6c9, 0x5c3, 0x4ca, 0x3c6, 0x2cf, 0x1c5, 0xcc ,
0xfcc, 0xec5, 0xdcf, 0xcc6, 0xbca, 0xac3, 0x9c9, 0x8c0,
0x8c0, 0x9c9, 0xac3, 0xbca, 0xcc6, 0xdcf, 0xec5, 0xfcc,
0xcc , 0x1c5, 0x2cf, 0x3c6, 0x4ca, 0x5c3, 0x6c9, 0x7c0,
0x950, 0x859, 0xb53, 0xa5a, 0xd56, 0xc5f, 0xf55, 0xe5c,
0x15c, 0x55 , 0x35f, 0x256, 0x55a, 0x453, 0x759, 0x650,
0xaf0, 0xbf9, 0x8f3, 0x9fa, 0xef6, 0xfff, 0xcf5, 0xdfc,
0x2fc, 0x3f5, 0xff , 0x1f6, 0x6fa, 0x7f3, 0x4f9, 0x5f0,
0xb60, 0xa69, 0x963, 0x86a, 0xf66, 0xe6f, 0xd65, 0xc6c,
0x36c, 0x265, 0x16f, 0x66 , 0x76a, 0x663, 0x569, 0x460,
0xca0, 0xda9, 0xea3, 0xfaa, 0x8a6, 0x9af, 0xaa5, 0xbac,
0x4ac, 0x5a5, 0x6af, 0x7a6, 0xaa , 0x1a3, 0x2a9, 0x3a0,
0xd30, 0xc39, 0xf33, 0xe3a, 0x936, 0x83f, 0xb35, 0xa3c,
0x53c, 0x435, 0x73f, 0x636, 0x13a, 0x33 , 0x339, 0x230,
0xe90, 0xf99, 0xc93, 0xd9a, 0xa96, 0xb9f, 0x895, 0x99c,
0x69c, 0x795, 0x49f, 0x596, 0x29a, 0x393, 0x99 , 0x190,
0xf00, 0xe09, 0xd03, 0xc0a, 0xb06, 0xa0f, 0x905, 0x80c,
0x70c, 0x605, 0x50f, 0x406, 0x30a, 0x203, 0x109, 0x0]

triTable = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[0, 8, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[0, 1, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[1, 8, 3, 9, 8, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[1, 2, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[0, 8, 3, 1, 2, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[9, 2, 10, 0, 2, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[2, 8, 3, 2, 10, 8, 10, 9, 8, -1, -1, -1, -1, -1, -1, -1],
[3, 11, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[0, 11, 2, 8, 11, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[1, 9, 0, 2, 3, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[1, 11, 2, 1, 9, 11, 9, 8, 11, -1, -1, -1, -1, -1, -1, -1],
[3, 10, 1, 11, 10, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[0, 10, 1, 0, 8, 10, 8, 11, 10, -1, -1, -1, -1, -1, -1, -1],
[3, 9, 0, 3, 11, 9, 11, 10, 9, -1, -1, -1, -1, -1, -1, -1],
[9, 8, 10, 10, 8, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[4, 7, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[4, 3, 0, 7, 3, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[0, 1, 9, 8, 4, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[4, 1, 9, 4, 7, 1, 7, 3, 1, -1, -1, -1, -1, -1, -1, -1],
[1, 2, 10, 8, 4, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[3, 4, 7, 3, 0, 4, 1, 2, 10, -1, -1, -1, -1, -1, -1, -1],
[9, 2, 10, 9, 0, 2, 8, 4, 7, -1, -1, -1, -1, -1, -1, -1],
[2, 10, 9, 2, 9, 7, 2, 7, 3, 7, 9, 4, -1, -1, -1, -1],
[8, 4, 7, 3, 11, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[11, 4, 7, 11, 2, 4, 2, 0, 4, -1, -1, -1, -1, -1, -1, -1],
[9, 0, 1, 8, 4, 7, 2, 3, 11, -1, -1, -1, -1, -1, -1, -1],
[4, 7, 11, 9, 4, 11, 9, 11, 2, 9, 2, 1, -1, -1, -1, -1],
[3, 10, 1, 3, 11, 10, 7, 8, 4, -1, -1, -1, -1, -1, -1, -1],
[1, 11, 10, 1, 4, 11, 1, 0, 4, 7, 11, 4, -1, -1, -1, -1],
[4, 7, 8, 9, 0, 11, 9, 11, 10, 11, 0, 3, -1, -1, -1, -1],
[4, 7, 11, 4, 11, 9, 9, 11, 10, -1, -1, -1, -1, -1, -1, -1],
[9, 5, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[9, 5, 4, 0, 8, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[0, 5, 4, 1, 5, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[8, 5, 4, 8, 3, 5, 3, 1, 5, -1, -1, -1, -1, -1, -1, -1],
[1, 2, 10, 9, 5, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[3, 0, 8, 1, 2, 10, 4, 9, 5, -1, -1, -1, -1, -1, -1, -1],
[5, 2, 10, 5, 4, 2, 4, 0, 2, -1, -1, -1, -1, -1, -1, -1],
[2, 10, 5, 3, 2, 5, 3, 5, 4, 3, 4, 8, -1, -1, -1, -1],
[9, 5, 4, 2, 3, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[0, 11, 2, 0, 8, 11, 4, 9, 5, -1, -1, -1, -1, -1, -1, -1],
[0, 5, 4, 0, 1, 5, 2, 3, 11, -1, -1, -1, -1, -1, -1, -1],
[2, 1, 5, 2, 5, 8, 2, 8, 11, 4, 8, 5, -1, -1, -1, -1],
[10, 3, 11, 10, 1, 3, 9, 5, 4, -1, -1, -1, -1, -1, -1, -1],
[4, 9, 5, 0, 8, 1, 8, 10, 1, 8, 11, 10, -1, -1, -1, -1],
[5, 4, 0, 5, 0, 11, 5, 11, 10, 11, 0, 3, -1, -1, -1, -1],
[5, 4, 8, 5, 8, 10, 10, 8, 11, -1, -1, -1, -1, -1, -1, -1],
[9, 7, 8, 5, 7, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[9, 3, 0, 9, 5, 3, 5, 7, 3, -1, -1, -1, -1, -1, -1, -1],
[0, 7, 8, 0, 1, 7, 1, 5, 7, -1, -1, -1, -1, -1, -1, -1],
[1, 5, 3, 3, 5, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[9, 7, 8, 9, 5, 7, 10, 1, 2, -1, -1, -1, -1, -1, -1, -1],
[10, 1, 2, 9, 5, 0, 5, 3, 0, 5, 7, 3, -1, -1, -1, -1],
[8, 0, 2, 8, 2, 5, 8, 5, 7, 10, 5, 2, -1, -1, -1, -1],
[2, 10, 5, 2, 5, 3, 3, 5, 7, -1, -1, -1, -1, -1, -1, -1],
[7, 9, 5, 7, 8, 9, 3, 11, 2, -1, -1, -1, -1, -1, -1, -1],
[9, 5, 7, 9, 7, 2, 9, 2, 0, 2, 7, 11, -1, -1, -1, -1],
[2, 3, 11, 0, 1, 8, 1, 7, 8, 1, 5, 7, -1, -1, -1, -1],
[11, 2, 1, 11, 1, 7, 7, 1, 5, -1, -1, -1, -1, -1, -1, -1],
[9, 5, 8, 8, 5, 7, 10, 1, 3, 10, 3, 11, -1, -1, -1, -1],
[5, 7, 0, 5, 0, 9, 7, 11, 0, 1, 0, 10, 11, 10, 0, -1],
[11, 10, 0, 11, 0, 3, 10, 5, 0, 8, 0, 7, 5, 7, 0, -1],
[11, 10, 5, 7, 11, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[10, 6, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[0, 8, 3, 5, 10, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[9, 0, 1, 5, 10, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[1, 8, 3, 1, 9, 8, 5, 10, 6, -1, -1, -1, -1, -1, -1, -1],
[1, 6, 5, 2, 6, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[1, 6, 5, 1, 2, 6, 3, 0, 8, -1, -1, -1, -1, -1, -1, -1],
[9, 6, 5, 9, 0, 6, 0, 2, 6, -1, -1, -1, -1, -1, -1, -1],
[5, 9, 8, 5, 8, 2, 5, 2, 6, 3, 2, 8, -1, -1, -1, -1],
[2, 3, 11, 10, 6, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[11, 0, 8, 11, 2, 0, 10, 6, 5, -1, -1, -1, -1, -1, -1, -1],
[0, 1, 9, 2, 3, 11, 5, 10, 6, -1, -1, -1, -1, -1, -1, -1],
[5, 10, 6, 1, 9, 2, 9, 11, 2, 9, 8, 11, -1, -1, -1, -1],
[6, 3, 11, 6, 5, 3, 5, 1, 3, -1, -1, -1, -1, -1, -1, -1],
[0, 8, 11, 0, 11, 5, 0, 5, 1, 5, 11, 6, -1, -1, -1, -1],
[3, 11, 6, 0, 3, 6, 0, 6, 5, 0, 5, 9, -1, -1, -1, -1],
[6, 5, 9, 6, 9, 11, 11, 9, 8, -1, -1, -1, -1, -1, -1, -1],
[5, 10, 6, 4, 7, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[4, 3, 0, 4, 7, 3, 6, 5, 10, -1, -1, -1, -1, -1, -1, -1],
[1, 9, 0, 5, 10, 6, 8, 4, 7, -1, -1, -1, -1, -1, -1, -1],
[10, 6, 5, 1, 9, 7, 1, 7, 3, 7, 9, 4, -1, -1, -1, -1],
[6, 1, 2, 6, 5, 1, 4, 7, 8, -1, -1, -1, -1, -1, -1, -1],
[1, 2, 5, 5, 2, 6, 3, 0, 4, 3, 4, 7, -1, -1, -1, -1],
[8, 4, 7, 9, 0, 5, 0, 6, 5, 0, 2, 6, -1, -1, -1, -1],
[7, 3, 9, 7, 9, 4, 3, 2, 9, 5, 9, 6, 2, 6, 9, -1],
[3, 11, 2, 7, 8, 4, 10, 6, 5, -1, -1, -1, -1, -1, -1, -1],
[5, 10, 6, 4, 7, 2, 4, 2, 0, 2, 7, 11, -1, -1, -1, -1],
[0, 1, 9, 4, 7, 8, 2, 3, 11, 5, 10, 6, -1, -1, -1, -1],
[9, 2, 1, 9, 11, 2, 9, 4, 11, 7, 11, 4, 5, 10, 6, -1],
[8, 4, 7, 3, 11, 5, 3, 5, 1, 5, 11, 6, -1, -1, -1, -1],
[5, 1, 11, 5, 11, 6, 1, 0, 11, 7, 11, 4, 0, 4, 11, -1],
[0, 5, 9, 0, 6, 5, 0, 3, 6, 11, 6, 3, 8, 4, 7, -1],
[6, 5, 9, 6, 9, 11, 4, 7, 9, 7, 11, 9, -1, -1, -1, -1],
[10, 4, 9, 6, 4, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[4, 10, 6, 4, 9, 10, 0, 8, 3, -1, -1, -1, -1, -1, -1, -1],
[10, 0, 1, 10, 6, 0, 6, 4, 0, -1, -1, -1, -1, -1, -1, -1],
[8, 3, 1, 8, 1, 6, 8, 6, 4, 6, 1, 10, -1, -1, -1, -1],
[1, 4, 9, 1, 2, 4, 2, 6, 4, -1, -1, -1, -1, -1, -1, -1],
[3, 0, 8, 1, 2, 9, 2, 4, 9, 2, 6, 4, -1, -1, -1, -1],
[0, 2, 4, 4, 2, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[8, 3, 2, 8, 2, 4, 4, 2, 6, -1, -1, -1, -1, -1, -1, -1],
[10, 4, 9, 10, 6, 4, 11, 2, 3, -1, -1, -1, -1, -1, -1, -1],
[0, 8, 2, 2, 8, 11, 4, 9, 10, 4, 10, 6, -1, -1, -1, -1],
[3, 11, 2, 0, 1, 6, 0, 6, 4, 6, 1, 10, -1, -1, -1, -1],
[6, 4, 1, 6, 1, 10, 4, 8, 1, 2, 1, 11, 8, 11, 1, -1],
[9, 6, 4, 9, 3, 6, 9, 1, 3, 11, 6, 3, -1, -1, -1, -1],
[8, 11, 1, 8, 1, 0, 11, 6, 1, 9, 1, 4, 6, 4, 1, -1],
[3, 11, 6, 3, 6, 0, 0, 6, 4, -1, -1, -1, -1, -1, -1, -1],
[6, 4, 8, 11, 6, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[7, 10, 6, 7, 8, 10, 8, 9, 10, -1, -1, -1, -1, -1, -1, -1],
[0, 7, 3, 0, 10, 7, 0, 9, 10, 6, 7, 10, -1, -1, -1, -1],
[10, 6, 7, 1, 10, 7, 1, 7, 8, 1, 8, 0, -1, -1, -1, -1],
[10, 6, 7, 10, 7, 1, 1, 7, 3, -1, -1, -1, -1, -1, -1, -1],
[1, 2, 6, 1, 6, 8, 1, 8, 9, 8, 6, 7, -1, -1, -1, -1],
[2, 6, 9, 2, 9, 1, 6, 7, 9, 0, 9, 3, 7, 3, 9, -1],
[7, 8, 0, 7, 0, 6, 6, 0, 2, -1, -1, -1, -1, -1, -1, -1],
[7, 3, 2, 6, 7, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[2, 3, 11, 10, 6, 8, 10, 8, 9, 8, 6, 7, -1, -1, -1, -1],
[2, 0, 7, 2, 7, 11, 0, 9, 7, 6, 7, 10, 9, 10, 7, -1],
[1, 8, 0, 1, 7, 8, 1, 10, 7, 6, 7, 10, 2, 3, 11, -1],
[11, 2, 1, 11, 1, 7, 10, 6, 1, 6, 7, 1, -1, -1, -1, -1],
[8, 9, 6, 8, 6, 7, 9, 1, 6, 11, 6, 3, 1, 3, 6, -1],
[0, 9, 1, 11, 6, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[7, 8, 0, 7, 0, 6, 3, 11, 0, 11, 6, 0, -1, -1, -1, -1],
[7, 11, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[7, 6, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[3, 0, 8, 11, 7, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[0, 1, 9, 11, 7, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[8, 1, 9, 8, 3, 1, 11, 7, 6, -1, -1, -1, -1, -1, -1, -1],
[10, 1, 2, 6, 11, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[1, 2, 10, 3, 0, 8, 6, 11, 7, -1, -1, -1, -1, -1, -1, -1],
[2, 9, 0, 2, 10, 9, 6, 11, 7, -1, -1, -1, -1, -1, -1, -1],
[6, 11, 7, 2, 10, 3, 10, 8, 3, 10, 9, 8, -1, -1, -1, -1],
[7, 2, 3, 6, 2, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[7, 0, 8, 7, 6, 0, 6, 2, 0, -1, -1, -1, -1, -1, -1, -1],
[2, 7, 6, 2, 3, 7, 0, 1, 9, -1, -1, -1, -1, -1, -1, -1],
[1, 6, 2, 1, 8, 6, 1, 9, 8, 8, 7, 6, -1, -1, -1, -1],
[10, 7, 6, 10, 1, 7, 1, 3, 7, -1, -1, -1, -1, -1, -1, -1],
[10, 7, 6, 1, 7, 10, 1, 8, 7, 1, 0, 8, -1, -1, -1, -1],
[0, 3, 7, 0, 7, 10, 0, 10, 9, 6, 10, 7, -1, -1, -1, -1],
[7, 6, 10, 7, 10, 8, 8, 10, 9, -1, -1, -1, -1, -1, -1, -1],
[6, 8, 4, 11, 8, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[3, 6, 11, 3, 0, 6, 0, 4, 6, -1, -1, -1, -1, -1, -1, -1],
[8, 6, 11, 8, 4, 6, 9, 0, 1, -1, -1, -1, -1, -1, -1, -1],
[9, 4, 6, 9, 6, 3, 9, 3, 1, 11, 3, 6, -1, -1, -1, -1],
[6, 8, 4, 6, 11, 8, 2, 10, 1, -1, -1, -1, -1, -1, -1, -1],
[1, 2, 10, 3, 0, 11, 0, 6, 11, 0, 4, 6, -1, -1, -1, -1],
[4, 11, 8, 4, 6, 11, 0, 2, 9, 2, 10, 9, -1, -1, -1, -1],
[10, 9, 3, 10, 3, 2, 9, 4, 3, 11, 3, 6, 4, 6, 3, -1],
[8, 2, 3, 8, 4, 2, 4, 6, 2, -1, -1, -1, -1, -1, -1, -1],
[0, 4, 2, 4, 6, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[1, 9, 0, 2, 3, 4, 2, 4, 6, 4, 3, 8, -1, -1, -1, -1],
[1, 9, 4, 1, 4, 2, 2, 4, 6, -1, -1, -1, -1, -1, -1, -1],
[8, 1, 3, 8, 6, 1, 8, 4, 6, 6, 10, 1, -1, -1, -1, -1],
[10, 1, 0, 10, 0, 6, 6, 0, 4, -1, -1, -1, -1, -1, -1, -1],
[4, 6, 3, 4, 3, 8, 6, 10, 3, 0, 3, 9, 10, 9, 3, -1],
[10, 9, 4, 6, 10, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[4, 9, 5, 7, 6, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[0, 8, 3, 4, 9, 5, 11, 7, 6, -1, -1, -1, -1, -1, -1, -1],
[5, 0, 1, 5, 4, 0, 7, 6, 11, -1, -1, -1, -1, -1, -1, -1],
[11, 7, 6, 8, 3, 4, 3, 5, 4, 3, 1, 5, -1, -1, -1, -1],
[9, 5, 4, 10, 1, 2, 7, 6, 11, -1, -1, -1, -1, -1, -1, -1],
[6, 11, 7, 1, 2, 10, 0, 8, 3, 4, 9, 5, -1, -1, -1, -1],
[7, 6, 11, 5, 4, 10, 4, 2, 10, 4, 0, 2, -1, -1, -1, -1],
[3, 4, 8, 3, 5, 4, 3, 2, 5, 10, 5, 2, 11, 7, 6, -1],
[7, 2, 3, 7, 6, 2, 5, 4, 9, -1, -1, -1, -1, -1, -1, -1],
[9, 5, 4, 0, 8, 6, 0, 6, 2, 6, 8, 7, -1, -1, -1, -1],
[3, 6, 2, 3, 7, 6, 1, 5, 0, 5, 4, 0, -1, -1, -1, -1],
[6, 2, 8, 6, 8, 7, 2, 1, 8, 4, 8, 5, 1, 5, 8, -1],
[9, 5, 4, 10, 1, 6, 1, 7, 6, 1, 3, 7, -1, -1, -1, -1],
[1, 6, 10, 1, 7, 6, 1, 0, 7, 8, 7, 0, 9, 5, 4, -1],
[4, 0, 10, 4, 10, 5, 0, 3, 10, 6, 10, 7, 3, 7, 10, -1],
[7, 6, 10, 7, 10, 8, 5, 4, 10, 4, 8, 10, -1, -1, -1, -1],
[6, 9, 5, 6, 11, 9, 11, 8, 9, -1, -1, -1, -1, -1, -1, -1],
[3, 6, 11, 0, 6, 3, 0, 5, 6, 0, 9, 5, -1, -1, -1, -1],
[0, 11, 8, 0, 5, 11, 0, 1, 5, 5, 6, 11, -1, -1, -1, -1],
[6, 11, 3, 6, 3, 5, 5, 3, 1, -1, -1, -1, -1, -1, -1, -1],
[1, 2, 10, 9, 5, 11, 9, 11, 8, 11, 5, 6, -1, -1, -1, -1],
[0, 11, 3, 0, 6, 11, 0, 9, 6, 5, 6, 9, 1, 2, 10, -1],
[11, 8, 5, 11, 5, 6, 8, 0, 5, 10, 5, 2, 0, 2, 5, -1],
[6, 11, 3, 6, 3, 5, 2, 10, 3, 10, 5, 3, -1, -1, -1, -1],
[5, 8, 9, 5, 2, 8, 5, 6, 2, 3, 8, 2, -1, -1, -1, -1],
[9, 5, 6, 9, 6, 0, 0, 6, 2, -1, -1, -1, -1, -1, -1, -1],
[1, 5, 8, 1, 8, 0, 5, 6, 8, 3, 8, 2, 6, 2, 8, -1],
[1, 5, 6, 2, 1, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[1, 3, 6, 1, 6, 10, 3, 8, 6, 5, 6, 9, 8, 9, 6, -1],
[10, 1, 0, 10, 0, 6, 9, 5, 0, 5, 6, 0, -1, -1, -1, -1],
[0, 3, 8, 5, 6, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[10, 5, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[11, 5, 10, 7, 5, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[11, 5, 10, 11, 7, 5, 8, 3, 0, -1, -1, -1, -1, -1, -1, -1],
[5, 11, 7, 5, 10, 11, 1, 9, 0, -1, -1, -1, -1, -1, -1, -1],
[10, 7, 5, 10, 11, 7, 9, 8, 1, 8, 3, 1, -1, -1, -1, -1],
[11, 1, 2, 11, 7, 1, 7, 5, 1, -1, -1, -1, -1, -1, -1, -1],
[0, 8, 3, 1, 2, 7, 1, 7, 5, 7, 2, 11, -1, -1, -1, -1],
[9, 7, 5, 9, 2, 7, 9, 0, 2, 2, 11, 7, -1, -1, -1, -1],
[7, 5, 2, 7, 2, 11, 5, 9, 2, 3, 2, 8, 9, 8, 2, -1],
[2, 5, 10, 2, 3, 5, 3, 7, 5, -1, -1, -1, -1, -1, -1, -1],
[8, 2, 0, 8, 5, 2, 8, 7, 5, 10, 2, 5, -1, -1, -1, -1],
[9, 0, 1, 5, 10, 3, 5, 3, 7, 3, 10, 2, -1, -1, -1, -1],
[9, 8, 2, 9, 2, 1, 8, 7, 2, 10, 2, 5, 7, 5, 2, -1],
[1, 3, 5, 3, 7, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[0, 8, 7, 0, 7, 1, 1, 7, 5, -1, -1, -1, -1, -1, -1, -1],
[9, 0, 3, 9, 3, 5, 5, 3, 7, -1, -1, -1, -1, -1, -1, -1],
[9, 8, 7, 5, 9, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[5, 8, 4, 5, 10, 8, 10, 11, 8, -1, -1, -1, -1, -1, -1, -1],
[5, 0, 4, 5, 11, 0, 5, 10, 11, 11, 3, 0, -1, -1, -1, -1],
[0, 1, 9, 8, 4, 10, 8, 10, 11, 10, 4, 5, -1, -1, -1, -1],
[10, 11, 4, 10, 4, 5, 11, 3, 4, 9, 4, 1, 3, 1, 4, -1],
[2, 5, 1, 2, 8, 5, 2, 11, 8, 4, 5, 8, -1, -1, -1, -1],
[0, 4, 11, 0, 11, 3, 4, 5, 11, 2, 11, 1, 5, 1, 11, -1],
[0, 2, 5, 0, 5, 9, 2, 11, 5, 4, 5, 8, 11, 8, 5, -1],
[9, 4, 5, 2, 11, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[2, 5, 10, 3, 5, 2, 3, 4, 5, 3, 8, 4, -1, -1, -1, -1],
[5, 10, 2, 5, 2, 4, 4, 2, 0, -1, -1, -1, -1, -1, -1, -1],
[3, 10, 2, 3, 5, 10, 3, 8, 5, 4, 5, 8, 0, 1, 9, -1],
[5, 10, 2, 5, 2, 4, 1, 9, 2, 9, 4, 2, -1, -1, -1, -1],
[8, 4, 5, 8, 5, 3, 3, 5, 1, -1, -1, -1, -1, -1, -1, -1],
[0, 4, 5, 1, 0, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[8, 4, 5, 8, 5, 3, 9, 0, 5, 0, 3, 5, -1, -1, -1, -1],
[9, 4, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[4, 11, 7, 4, 9, 11, 9, 10, 11, -1, -1, -1, -1, -1, -1, -1],
[0, 8, 3, 4, 9, 7, 9, 11, 7, 9, 10, 11, -1, -1, -1, -1],
[1, 10, 11, 1, 11, 4, 1, 4, 0, 7, 4, 11, -1, -1, -1, -1],
[3, 1, 4, 3, 4, 8, 1, 10, 4, 7, 4, 11, 10, 11, 4, -1],
[4, 11, 7, 9, 11, 4, 9, 2, 11, 9, 1, 2, -1, -1, -1, -1],
[9, 7, 4, 9, 11, 7, 9, 1, 11, 2, 11, 1, 0, 8, 3, -1],
[11, 7, 4, 11, 4, 2, 2, 4, 0, -1, -1, -1, -1, -1, -1, -1],
[11, 7, 4, 11, 4, 2, 8, 3, 4, 3, 2, 4, -1, -1, -1, -1],
[2, 9, 10, 2, 7, 9, 2, 3, 7, 7, 4, 9, -1, -1, -1, -1],
[9, 10, 7, 9, 7, 4, 10, 2, 7, 8, 7, 0, 2, 0, 7, -1],
[3, 7, 10, 3, 10, 2, 7, 4, 10, 1, 10, 0, 4, 0, 10, -1],
[1, 10, 2, 8, 7, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[4, 9, 1, 4, 1, 7, 7, 1, 3, -1, -1, -1, -1, -1, -1, -1],
[4, 9, 1, 4, 1, 7, 0, 8, 1, 8, 7, 1, -1, -1, -1, -1],
[4, 0, 3, 7, 4, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[4, 8, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[9, 10, 8, 10, 11, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[3, 0, 9, 3, 9, 11, 11, 9, 10, -1, -1, -1, -1, -1, -1, -1],
[0, 1, 10, 0, 10, 8, 8, 10, 11, -1, -1, -1, -1, -1, -1, -1],
[3, 1, 10, 11, 3, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[1, 2, 11, 1, 11, 9, 9, 11, 8, -1, -1, -1, -1, -1, -1, -1],
[3, 0, 9, 3, 9, 11, 1, 2, 9, 2, 11, 9, -1, -1, -1, -1],
[0, 2, 11, 8, 0, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[3, 2, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[2, 3, 8, 2, 8, 10, 10, 8, 9, -1, -1, -1, -1, -1, -1, -1],
[9, 10, 2, 0, 9, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[2, 3, 8, 2, 8, 10, 0, 1, 8, 1, 10, 8, -1, -1, -1, -1],
[1, 10, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[1, 3, 8, 9, 1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[0, 9, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[0, 3, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]
