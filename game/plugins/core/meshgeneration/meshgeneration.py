from voxel import Voxel
from dual import DualContour
from marching import MarchingCubes

from panda3d.core import GeomVertexFormat
from panda3d.core import GeomVertexData
from panda3d.core import GeomVertexWriter
from panda3d.core import GeomTriangles
from panda3d.core import GeomNode
from panda3d.core import Geom

import math
import random


class MeshGeneration:
    """MeshGeneration for the chunks"""
    def __init__(self, manager, xml):
        self.reload(manager, xml)

    def reload(self, manager, xml):
        self.meshgentype = xml.get('gentype')
        print "DEBUG: " + self.meshgentype

    def start(self):
        pass

    def stop(self):
        pass

    def destroy(self):
        pass

    def getGenType(self):
        return self.meshgentype

    def generate(self, terrain, size, lod=1.0):
        if self.meshgentype == "marching":
            mesher = MarchingCubes()
        elif self.meshgentype == "dual":
            mesher = DualContour()
        else:
            mesher = Voxel()

        triangles = mesher.generateMesh(terrain, size, lod)

        #format = GeomVertexFormat.registerFormat(GeomVertexFormat.getV3n3c4t2())
        format = GeomVertexFormat.registerFormat(GeomVertexFormat.getV3n3c4())
        vdata = GeomVertexData('chunk_mesh', format, Geom.UHStatic)

        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color = GeomVertexWriter(vdata, 'color')
        texcoord = GeomVertexWriter(vdata, 'texcoord')
        prim = GeomTriangles(Geom.UHStatic)

        vertexcount = 0
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
                #color.addData4f(random.randrange(0,255), random.randrange(0,255), random.randrange(0,255), 1)
                #texcoord.addData2f(triangle[0][0] / 16, triangle[0][1] / 16)
                #texcoord.addData2f(0, 1)

            #make triangles
            prim.addVertices(vertexcount, vertexcount + 1, vertexcount + 2)
            prim.closePrimitive()
            vertexcount += 3

        #print prim
        #attach primitives and render
        geom = Geom(vdata)
        geom.addPrimitive(prim)

        """try:
            self.node.removeNode()
            self.bulletnode.removeShape(self.bulletshape)
            self.root.bulletworld.removeRigidBody(self.bulletnode)
            self.bulletnp.removeNode()
        except AttributeError:
            pass"""

        node = GeomNode("terrainmesh")
        node.addGeom(geom)
        return node

        #self.meshed = True

        """#do bullet meshing
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
        self.root.bulletworld.attachRigidBody(self.bulletnode)"""
