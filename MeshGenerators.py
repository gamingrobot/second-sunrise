#Meshgenerators.py
import Util

import numpy as np
import math
from Blocks import *

import numpy.linalg as la
#import scipy.optimize as opt
#import itertools as it
import math

isovalue = 0


class Voxel:
    def __init__(self, chunk, size, chunks, pradius, noise):
        self.blocks = chunk.blocks
        self.x = chunk.x
        self.y = chunk.y
        self.z = chunk.z
        self.size = size
        self.level = float(isovalue)
        self.triangles = []
        self.chunks = chunks
        self.radius = pradius
        self.noise = noise

    def generateMesh(self):
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
                            #self.triangles.append([[], [], []])
                            self.triangles.append([[x, y, z], [x, y, z + 1], [x, y + 1, z + 1]])
                            self.triangles.append([[x, y + 1, z + 1], [x, y + 1, z], [x, y, z]])
                        #front
                        block = None
                        if y >= 1:
                            block = self.blocks[x, y - 1, z]
                        if self.isEmptyBlock(block):
                            self.triangles.append([[x + 1, y, z], [x + 1, y, z + 1], [x, y, z + 1]])
                            self.triangles.append([[x, y, z + 1], [x, y, z], [x + 1, y, z]])
                        #right
                        block = None
                        if x < self.size - 1:
                            block = self.blocks[x + 1, y, z]
                        if self.isEmptyBlock(block):
                            self.triangles.append([[x + 1, y + 1, z + 1], [x + 1, y, z + 1], [x + 1, y, z]])
                            self.triangles.append([[x + 1, y, z], [x + 1, y + 1, z], [x + 1, y + 1, z + 1]])
                        #back
                        block = None
                        if y < self.size - 1:
                            block = self.blocks[x, y + 1, z]
                        if self.isEmptyBlock(block):
                            self.triangles.append([[x, y + 1, z + 1], [x + 1, y + 1, z + 1], [x + 1, y + 1, z]])
                            self.triangles.append([[x + 1, y + 1, z], [x, y + 1, z], [x, y + 1, z + 1]])
                        #bottom
                        block = None
                        if z > 1:
                            block = self.blocks[x, y, z - 1]
                        if self.isEmptyBlock(block):
                            self.triangles.append([[x, y + 1, z], [x + 1, y + 1, z], [x + 1, y, z]])
                            self.triangles.append([[x + 1, y, z], [x, y, z], [x, y + 1, z]])
                        #top
                        block = None
                        if z < self.size - 1:
                            block = self.blocks[x, y, z + 1]
                        if self.isEmptyBlock(block):
                            self.triangles.append([[x + 1, y, z + 1], [x + 1, y + 1, z + 1], [x, y + 1, z + 1]])
                            self.triangles.append([[x, y + 1, z + 1], [x, y, z + 1], [x + 1, y, z + 1]])
        return self.triangles

    def isEmptyBlock(self, block):
        if block == None:
            return True
        elif block.__class__.__name__ != "Air" and block.__class__.__name__ != "Space":
            return False
        else:
            return True


class DualContour:
    def __init__(self, chunk, size, chunks, pradius, noise):
        self.blocks = chunk.blocks
        self.x = chunk.x
        self.y = chunk.y
        self.z = chunk.z
        self.size = size
        self.level = float(isovalue)
        self.triangles = []
        self.chunks = chunks
        self.radius = pradius
        self.noise = noise

        self.center = np.array([16, 16, 16])
        self.radius = 5

        #Cardinal directions
        self.dirs = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

        #Vertices of cube
        self.cube_verts = [np.array([x, y, z])
            for x in range(2)
            for y in range(2)
            for z in range(2)]

    def generateMesh(self):
        for x in xrange(0, self.size - 1):
            for y in xrange(0, self.size - 1):
                for z in xrange(0, self.size - 1):
                    #Solve qef to get vertex
                    A = [n for p, n in h_data]
                    b = [np.dot(p, n) for p, n in h_data]
                    v, residue, rank, s = la.lstsq(A, b)

                    #Throw out failed solutions
                    if la.norm(v - o) > 2:
                        continue

                    #Emit one vertex per every cube that crosses
                    vindex[tuple(o)] = len(dc_verts)
                    dc_verts.append(v)

                #Construct faces
                dc_faces = []
                for x, y, z in it.product(range(nc), range(nc), range(nc)):
                    if not (x, y, z) in vindex:
                        continue

                    #Emit one face per each edge that crosses
                    o = np.array([x, y, z])
                    for i in range(3):
                        for j in range(i):
                            if mask & 1:
                                dc_faces.append((vindex[tuple(o)], vindex[tuple(o + self.dirs[i])], vindex[tuple(o + self.dirs[j])]))
                                dc_faces.append((vindex[tuple(o + self.dirs[i] + self.dirs[j])], vindex[tuple(o + self.dirs[j])], vindex[tuple(o + self.dirs[i])]))
                            else:
                                dc_faces.append((vindex[tuple(o + self.dirs[j])], vindex[tuple(o + self.dirs[i])], vindex[tuple(o)]))
                                dc_faces.append((vindex[tuple(o + self.dirs[i])], vindex[tuple(o + self.dirs[j])], vindex[tuple(o + self.dirs[i] + self.dirs[j])]))

        dc_triangles = []
        for face in dc_faces:
            v1 = dc_verts[face[0]]
            v2 = dc_verts[face[1]]
            v3 = dc_verts[face[2]]
            dc_triangles.append(((v1[0], v1[1], v1[2]),
                (v2[0], v2[1], v2[2]),
                (v3[0], v3[1], v3[2])))
        return dc_triangles


class MarchingCubes:

    class GridCell:
        def __init__(self):
            self.position = [(0.0, 0.0, 0.0) for i in range(8)]
            self.value = None

    def __init__(self, chunk, size, chunks, pradius, noise):
        self.blocks = chunk.blocks
        self.x = chunk.x
        self.y = chunk.y
        self.z = chunk.z
        self.size = size
        self.level = float(isovalue)
        self.triangles = []
        self.chunks = chunks
        self.radius = pradius
        self.noise = noise

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

    def generateMesh(self):
        #triangles = []
        for x in xrange(0, self.size):
            for y in xrange(0, self.size):
                for z in xrange(0, self.size):
                    #Thread.forceYield()
                    p = self.GridCell()
                    pv = []
                    position = p.position
                    #(x, y, z) = (float(i), float(j), float(k))
                    """position[0] = (x, y, z)
                    position[1] = (x + 1, y, z)
                    position[2] = (x + 1, y + 1, z)
                    position[3] = (x, y + 1, z)
                    position[4] = (x, y, z + 1)
                    position[5] = (x + 1, y, z + 1)
                    position[6] = (x + 1, y + 1, z + 1)
                    position[7] = (x, y + 1, z + 1)"""
                    position[0] = (x + 0.5, y + 0.5, z + 0.5)
                    position[1] = (x + 1.5, y + 0.5, z + 0.5)
                    position[2] = (x + 1.5, y + 1.5, z + 0.5)
                    position[3] = (x + 0.5, y + 1.5, z + 0.5)
                    position[4] = (x + 0.5, y + 0.5, z + 1.5)
                    position[5] = (x + 1.5, y + 0.5, z + 1.5)
                    position[6] = (x + 1.5, y + 1.5, z + 1.5)
                    position[7] = (x + 0.5, y + 1.5, z + 1.5)

                    if x == self.size - 1 and y == self.size - 1 and z == self.size - 1:
                        currentdensity = self.blocks[x, y, z].getDensity()
                        pv.append(currentdensity)
                        ch = Util.genHash(self.x + 16, self.y, self.z)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[0, 15, 15].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x + 1, y, z), self.radius, self.noise))

                        ch = Util.genHash(self.x + 16, self.y + 16, self.z)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[0, 0, 15].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x + 1, y + 1, z), self.radius, self.noise))

                        ch = Util.genHash(self.x, self.y + 16, self.z)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[15, 0, 15].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x, y + 1, z), self.radius, self.noise))

                        ch = Util.genHash(self.x, self.y, self.z + 16)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[15, 15, 0].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x, y, z + 1), self.radius, self.noise))

                        ch = Util.genHash(self.x + 16, self.y, self.z + 16)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[0, 15, 0].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x + 1, y, z + 1), self.radius, self.noise))

                        ch = Util.genHash(self.x + 16, self.y + 16, self.z + 16)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[0, 0, 0].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x + 1, y + 1, z + 1), self.radius, self.noise))

                        ch = Util.genHash(self.x, self.y + 16, self.z + 16)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[15, 0, 0].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x, y + 1, z + 1), self.radius, self.noise))

                    elif x == self.size - 1 and y == self.size - 1:
                        currentdensity = self.blocks[x, y, z].getDensity()
                        pv.append(currentdensity)
                        ch = Util.genHash(self.x + 16, self.y, self.z)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[0, 15, z].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x + 1, y, z), self.radius, self.noise))
                        ch = Util.genHash(self.x + 16, self.y + 16, self.z)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[0, 0, z].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x + 1, y + 1, z), self.radius, self.noise))
                        ch = Util.genHash(self.x, self.y + 16, self.z)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[15, 0, z].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x, y + 1, z), self.radius, self.noise))
                        pv.append(self.blocks[x, y, z + 1].getDensity())
                        ch = Util.genHash(self.x + 16, self.y, self.z)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[0, 15, z + 1].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x + 1, y, z + 1), self.radius, self.noise))
                        ch = Util.genHash(self.x + 16, self.y + 16, self.z)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[0, 0, z + 1].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x + 1, y + 1, z + 1), self.radius, self.noise))
                        ch = Util.genHash(self.x, self.y + 16, self.z)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[15, 0, z + 1].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x, y + 1, z + 1), self.radius, self.noise))

                    elif x == self.size - 1 and z == self.size - 1:
                        currentdensity = self.blocks[x, y, z].getDensity()
                        pv.append(currentdensity)
                        ch = Util.genHash(self.x + 16, self.y, self.z)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[0, y, 15].getDensity())
                            pv.append(self.chunks[ch].blocks[0, y + 1, 15].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x + 1, y, z), self.radius, self.noise))
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x + 1, y + 1, z), self.radius, self.noise))
                        pv.append(self.blocks[x, y + 1, z].getDensity())
                        ch = Util.genHash(self.x, self.y, self.z + 16)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[15, y, 0].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x, y, z + 1), self.radius, self.noise))
                        ch = Util.genHash(self.x + 16, self.y, self.z + 16)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[0, y, 0].getDensity())
                            pv.append(self.chunks[ch].blocks[0, y + 1, 0].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x + 1, y, z + 1), self.radius, self.noise))
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x + 1, y + 1, z + 1), self.radius, self.noise))
                        ch = Util.genHash(self.x, self.y, self.z + 16)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[15, y + 1, 0].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x, y + 1, z + 1), self.radius, self.noise))

                    elif y == self.size - 1 and z == self.size - 1:
                        currentdensity = self.blocks[x, y, z].getDensity()
                        pv.append(currentdensity)
                        pv.append(self.blocks[x + 1, y, z].getDensity())
                        ch = Util.genHash(self.x, self.y + 16, self.z)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[x + 1, 0, 15].getDensity())
                            pv.append(self.chunks[ch].blocks[x, 0, 15].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x + 1, y + 1, z), self.radius, self.noise))
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x, y + 1, z), self.radius, self.noise))
                        ch = Util.genHash(self.x, self.y, self.z + 16)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[x, 15, 0].getDensity())
                            pv.append(self.chunks[ch].blocks[x + 1, 15, 0].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x, y, z + 1), self.radius, self.noise))
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x + 1, y, z + 1), self.radius, self.noise))
                        ch = Util.genHash(self.x, self.y + 16, self.z + 16)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[x + 1, 0, 0].getDensity())
                            pv.append(self.chunks[ch].blocks[x, 0, 0].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x + 1, y + 1, z + 1), self.radius, self.noise))
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x, y + 1, z + 1), self.radius, self.noise))

                    elif x == self.size - 1:
                        currentdensity = self.blocks[x, y, z].getDensity()
                        pv.append(currentdensity)
                        ch = Util.genHash(self.x + 16, self.y, self.z)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[0, y, z].getDensity())
                            pv.append(self.chunks[ch].blocks[0, y + 1, z].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x + 1, y, z), self.radius, self.noise))
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x + 1, y + 1, z), self.radius, self.noise))
                        pv.append(self.blocks[x, y + 1, z].getDensity())
                        pv.append(self.blocks[x, y, z + 1].getDensity())
                        ch = Util.genHash(self.x + 16, self.y, self.z)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[0, y, z + 1].getDensity())
                            pv.append(self.chunks[ch].blocks[0, y + 1, z + 1].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x + 1, y, z + 1), self.radius, self.noise))
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x + 1, y + 1, z + 1), self.radius, self.noise))
                        pv.append(self.blocks[x, y + 1, z + 1].getDensity())

                    elif y == self.size - 1:
                        currentdensity = self.blocks[x, y, z].getDensity()
                        pv.append(currentdensity)
                        pv.append(self.blocks[x + 1, y, z].getDensity())
                        ch = Util.genHash(self.x, self.y + 16, self.z)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[x + 1, 0, z].getDensity())
                            pv.append(self.chunks[ch].blocks[x, 0, z].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x + 1, y + 1, z), self.radius, self.noise))
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x, y + 1, z), self.radius, self.noise))
                        pv.append(self.blocks[x, y, z + 1].getDensity())
                        pv.append(self.blocks[x + 1, y, z + 1].getDensity())
                        ch = Util.genHash(self.x, self.y + 16, self.z)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[x + 1, 0, z + 1].getDensity())
                            pv.append(self.chunks[ch].blocks[x, 0, z + 1].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x + 1, y + 1, z + 1), self.radius, self.noise))
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x, y + 1, z + 1), self.radius, self.noise))

                    elif z == self.size - 1:
                        currentdensity = self.blocks[x, y, z].getDensity()
                        pv.append(currentdensity)
                        pv.append(self.blocks[x + 1, y, z].getDensity())
                        pv.append(self.blocks[x + 1, y + 1, z].getDensity())
                        pv.append(self.blocks[x, y + 1, z].getDensity())
                        ch = Util.genHash(self.x, self.y, self.z + 16)
                        if ch in self.chunks and self.chunks[ch].blocks != None:
                            pv.append(self.chunks[ch].blocks[x, y, 0].getDensity())
                            pv.append(self.chunks[ch].blocks[x + 1, y, 0].getDensity())
                            pv.append(self.chunks[ch].blocks[x + 1, y + 1, 0].getDensity())
                            pv.append(self.chunks[ch].blocks[x, y + 1, 0].getDensity())
                        else:
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x, y, z + 1), self.radius, self.noise))
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x + 1, y, z + 1), self.radius, self.noise))
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x + 1, y + 1, z + 1), self.radius, self.noise))
                            pv.append(Util.getDensity((self.x, self.y, self.z), (x, y + 1, z + 1), self.radius, self.noise))

                    else:
                        pv.append(self.blocks[x, y, z].getDensity())
                        pv.append(self.blocks[x + 1, y, z].getDensity())
                        pv.append(self.blocks[x + 1, y + 1, z].getDensity())
                        pv.append(self.blocks[x, y + 1, z].getDensity())
                        pv.append(self.blocks[x, y, z + 1].getDensity())
                        pv.append(self.blocks[x + 1, y, z + 1].getDensity())
                        pv.append(self.blocks[x + 1, y + 1, z + 1].getDensity())
                        pv.append(self.blocks[x, y + 1, z + 1].getDensity())

                    p.value = (pv[0], pv[1], pv[2], pv[3], pv[4], pv[5], pv[6], pv[7])
                    self.cube(p)
        #print self.triangles
        return self.triangles


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
