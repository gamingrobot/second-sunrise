#PlanetCraft.py
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile
from panda3d.core import GeomVertexFormat
from panda3d.core import GeomVertexData
from panda3d.core import GeomVertexWriter
from panda3d.core import GeomTriangles
from panda3d.core import GeomNode
from panda3d.core import Geom
import numpy as np

loadPrcFile("config/Config.prc")

class PlanetCraft(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        format = GeomVertexFormat.registerFormat(GeomVertexFormat.getV3n3c4t2())
        vdata = GeomVertexData('chunk', format, Geom.UHStatic)

        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color = GeomVertexWriter(vdata, 'color')
        texcoord = GeomVertexWriter(vdata, 'texcoord')

        #0
        vertex.addData3f(1, 0, 0)
        normal.addData3f(0, 0, 1)
        color.addData4f(0, 0, 1, 1)
        texcoord.addData2f(1, 0)
        #1
        vertex.addData3f(1, 1, 0)
        normal.addData3f(0, 0, 1)
        color.addData4f(0, 0, 1, 1)
        texcoord.addData2f(1, 1)
        #2
        vertex.addData3f(0, 1, 0)
        normal.addData3f(0, 0, 1)
        color.addData4f(0, 0, 1, 1)
        texcoord.addData2f(0, 1)
        #3
        vertex.addData3f(0, 0, 0)
        normal.addData3f(0, 0, 1)
        color.addData4f(0, 0, 1, 1)
        texcoord.addData2f(0, 0)

        #register primitives
        prim = GeomTriangles(Geom.UHStatic)
        #topside
        prim.addVertices(0, 1, 2)
        prim.addVertices(2, 3, 0)

        #attach primitives and render
        geom = Geom(vdata)
        geom.addPrimitive(prim)

        node = GeomNode('gnode')
        node.addGeom(geom)

        nodePath = self.render.attachNewNode(node)
        nodePath.setPos(0, 0, 0)

        #generate entire chunk node
        #store data in chunk class so dont have to regenerate

        #add to renderer

        #go onto next chunk

        """# INIT THE ARRAY OF BLOCKS
        self.chunksize = 8
        self.blocks = np.zeros((self.chunksize, self.chunksize, self.chunksize), dtype=np.object)
        it = np.nditer(self.blocks, op_flags=['readwrite'], flags=['multi_index', 'refs_ok'])
        while not it.finished:
            index = it.multi_index
            temp = self.loader.loadModel("models/box")
            temp.reparentTo(self.render)
            temp.setPos(index[0], index[1], index[2])
            it[0] = temp
            it.iternext()"""

        """##get data out of the array
        it = np.nditer(self.blocks, op_flags=['readwrite'], flags=['multi_index', 'refs_ok'])
        while not it.finished:
            index = it.multi_index
            temp = it[0].tolist()
            print temp.getPos()
            it.iternext()"""

app = PlanetCraft()
app.run()
