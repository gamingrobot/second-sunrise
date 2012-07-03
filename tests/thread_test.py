#bullet physics engine hello world with Panda3D

#from direct.directbase.DirectStart import *
from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeomVertexFormat
from panda3d.core import GeomVertexData
from panda3d.core import GeomVertexWriter
from panda3d.core import GeomTriangles
from panda3d.core import GeomNode
from panda3d.core import Geom
from direct.stdpy import threading
from pandac.PandaModules import Thread
from panda3d.core import loadPrcFile

loadPrcFile("Config.prc")


class ThreadingTest(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        #self.taskMgr.add(self.threadtest, 'thread')
        t = threading.Thread(target=self.threadtest, args=())
        t.start()

    # Update
    def threadtest(self):
        print "Started thread"
        format = GeomVertexFormat.registerFormat(GeomVertexFormat.getV3n3c4t2())
        vdata = GeomVertexData('chunk', format, Geom.UHStatic)

        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color = GeomVertexWriter(vdata, 'color')
        texcoord = GeomVertexWriter(vdata, 'texcoord')

        prim = GeomTriangles(Geom.UHStatic)
        self.vertexcount = 0

        shade = 0.9
        for x in range(10):
            #line corners
            #0
            vertex.addData3f(1, 0, 1)
            normal.addData3f(0, 0, 1)
            color.addData4f(shade, shade, shade, 1)
            texcoord.addData2f(1, 0)
            #1
            vertex.addData3f(0, 1, 1)
            normal.addData3f(0, 0, 1)
            color.addData4f(shade, shade, shade, 1)
            texcoord.addData2f(0, 1)
            #edge corners
            #22
            vertex.addData3f(1, 1, 1)
            normal.addData3f(0, 0, 1)
            color.addData4f(shade, shade, shade, 1)
            texcoord.addData2f(1, 1)
            #3
            vertex.addData3f(0, 0, 1)
            normal.addData3f(0, 0, 1)
            color.addData4f(shade, shade, shade, 1)
            texcoord.addData2f(0, 0)
            #draw triangles
            prim.addVertices(self.vertexcount, self.vertexcount + 2, self.vertexcount + 1)
            prim.addVertices(self.vertexcount + 1, self.vertexcount + 3, self.vertexcount)
            #increment vertexcount
            self.vertexcount += 4

        geom = Geom(vdata)
        geom.addPrimitive(prim)

        node = GeomNode('gnode')
        node.addGeom(geom)
        self.node = self.render.attachNewNode(node)
        self.node.setPos(0, 0, 0)
        print "Finished meshing"

app = ThreadingTest()
app.run()
