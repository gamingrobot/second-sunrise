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
from pandac.PandaModules import TexGenAttrib
from pandac.PandaModules import Texture
from pandac.PandaModules import TextureStage

import Util

from Util import MeshType

import numpy as np
import math
from Blocks import *
from MeshGenerators import *

isovalue = 0.0


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
        self.blocks = None
        self.noise = args['noise']

    def getChunkID(self):
        return self.id

    def generateBlocks(self):
        self.size = self.planet.chunkSize
        self.numchunks = self.planet.psize
        self.radius = self.planet.radius  # in blocks
        self.blocks = np.zeros((self.size, self.size, self.size), dtype=np.object)
        self.blockSize = 1
        #init numpy
        it = np.nditer(self.blocks, op_flags=['readwrite'], flags=['multi_index', 'refs_ok'])
        while not it.finished:
            index = it.multi_index
            den = Util.getDensity((self.x, self.y, self.z), (index[0], index[1], index[2]), self.radius, self.noise)
            if den >= isovalue:
                self.empty = False
                it[0] = Dirt(
                    {'x': index[0], 'y': index[1], 'z': index[2], 'density': float(den), 'name': '000'})
            else:
                it[0] = Air(
                    {'x': index[0], 'y': index[1], 'z': index[2], 'density': float(den), 'name': '000'})
            it.iternext()

    def removeBlock(self, x, y, z):
        print "removing" + str(x) + "," + str(y) + "," + str(z)
        print self.blocks[x][y][z]
        self.blocks[x][y][z] = Air(
                    {'x': x, 'y': y, 'z': z, 'density': float(-1.0), 'name': '000'})

    def placeBlock(self, x, y, z):
        print "placing" + str(x) + "," + str(y) + "," + str(z)
        print self.blocks[x][y][z]
        self.blocks[x][y][z] = Dirt(
                    {'x': x, 'y': y, 'z': z, 'density': float(1.0), 'name': '000'})

    def isEmpty(self):
        return self.empty

    def meshGenerated(self):
        return self.meshed

    def generateMesh(self, meshtype):
        print "Generating Chunk " + self.id
        self.chunks = self.planet.chunks
        if meshtype == MeshType.MarchingCubes:
            mesher = MarchingCubes(self, self.size, self.chunks, self.radius, self.noise)
        elif meshtype == MeshType.SurfaceNet:
            mesher = SurfaceNet(self, self.size, self.chunks, self.radius, self.noise)
        else:
            mesher = Voxel(self, self.size, self.chunks, self.radius, self.noise)

        triangles = mesher.generateMesh()

        #format = GeomVertexFormat.registerFormat(GeomVertexFormat.getV3n3c4t2())
        format = GeomVertexFormat.registerFormat(GeomVertexFormat.getV3n3c4())
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
                if normlength != 0:
                    normx /= normlength
                    normy /= normlength
                    normz /= normlength

                normal.addData3f(normx, normy, normz)
                color.addData4f(shade, shade, shade, 1)
                #texcoord.addData2f(triangle[0][0] / 16, triangle[0][1] / 16)
                #texcoord.addData2f(0, 1)

            #make triangles
            prim.addVertices(self.vertexcount, self.vertexcount + 1, self.vertexcount + 2)
            prim.closePrimitive()
            self.vertexcount += 3

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
        tex = loader.loadTexture("media/stone.jpg")
        tex.setMinfilter(Texture.FTLinearMipmapLinear)
        tex.setMagfilter(Texture.FTLinearMipmapLinear)
        tex.setAnisotropicDegree(2)
        tex.setWrapU(Texture.WMRepeat)
        tex.setWrapV(Texture.WMRepeat)
        self.node = self.planetNode.attachNewNode(node)
        self.node.setPos(self.x, self.y, self.z)
        self.node.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
        self.node.setTexture(tex)
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
        self.bulletnp.setPos(self.x, self.y, self.z)
        self.bulletnp.setCollideMask(BitMask32.allOn())
        self.root.bulletworld.attachRigidBody(self.bulletnode)
