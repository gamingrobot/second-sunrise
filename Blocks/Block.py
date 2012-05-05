#Base Class : Block
import random
import ogre.renderer.OGRE as ogre


class Block:
    """Block is a modifyable object"""
    def __init__(self, args):
        self.x = args['x']
        self.y = args['y']
        self.z = args['z']
        self.texture = 'Blocks/' + args['texture']
        #cn = args['chunkNode']
        randomnum = str(random.random())
        sm = args['senemanager']
        #cube = sm.createEntity(randomnum, 'cube.mesh')
        #cube.setMaterialName(self.texture)
        #node = cn.createChildSceneNode(args['texture'] + randomnum, ogre.Vector3(self.x, self.y, self.z))
        #node.attachObject(cube)




        testBox = self.createCubeMesh("TestBoxMesh", "")
        headNode = sm.getRootSceneNode().createChildSceneNode()
        Mesh = testBox.convertToMesh("TestBox")
        pEnt = sm.createEntity("TestBox")
        headNode.attachObject(pEnt)

    def __str__(self):
        return "Block: %s is at (%i, %i, %i)" % (self.__class__.__name__, self.x, self.y, self.z)

    def createCubeMesh(self, name, matName):
        cube = ogre.ManualObject(name)
        cube.begin(matName)

        cube.position(0.5, -0.5, 1.0)
        cube.normal(0.408248, -0.816497, 0.408248)
        cube.textureCoord(1, 0)
        cube.position(-0.5, -0.5, 0.0)
        cube.normal(-0.408248, -0.816497, -0.408248)
        cube.textureCoord(0, 1)
        cube.position(0.5, -0.5, 0.0)
        cube.normal(0.666667, -0.333333, -0.666667)
        cube.textureCoord(1, 1)
        cube.position(-0.5, -0.5, 1.0)
        cube.normal(-0.666667, -0.333333, 0.666667)
        cube.textureCoord(0, 0)
        cube.position(0.5, 0.5, 1.0)
        cube.normal(0.666667, 0.333333, 0.666667)
        cube.textureCoord(1, 0)
        cube.position(-0.5, -0.5, 1.0)
        cube.normal(-0.666667, -0.333333, 0.666667)
        cube.textureCoord(0, 1)
        cube.position(0.5, -0.5, 1.0)
        cube.normal(0.408248, -0.816497, 0.408248)
        cube.textureCoord(1, 1)
        cube.position(-0.5, 0.5, 1.0)
        cube.normal(-0.408248, 0.816497, 0.408248)
        cube.textureCoord(0, 0)
        cube.position(-0.5, 0.5, 0.0)
        cube.normal(-0.666667, 0.333333, -0.666667)
        cube.textureCoord(0, 1)
        cube.position(-0.5, -0.5, 0.0)
        cube.normal(-0.408248, -0.816497, -0.408248)
        cube.textureCoord(1, 1)
        cube.position(-0.5, -0.5, 1.0)
        cube.normal(-0.666667, -0.333333, 0.666667)
        cube.textureCoord(1, 0)
        cube.position(0.5, -0.5, 0.0)
        cube.normal(0.666667, -0.333333, -0.666667)
        cube.textureCoord(0, 1)
        cube.position(0.5, 0.5, 0.0)
        cube.normal(0.408248, 0.816497, -0.408248)
        cube.textureCoord(1, 1)
        cube.position(0.5, -0.5, 1.0)
        cube.normal(0.408248, -0.816497, 0.408248)
        cube.textureCoord(0, 0)
        cube.position(0.5, -0.5, 0.0)
        cube.normal(0.666667, -0.333333, -0.666667)
        cube.textureCoord(1, 0)
        cube.position(-0.5, -0.5, 0.0)
        cube.normal(-0.408248, -0.816497, -0.408248)
        cube.textureCoord(0, 0)
        cube.position(-0.5, 0.5, 1.0)
        cube.normal(-0.408248, 0.816497, 0.408248)
        cube.textureCoord(1, 0)
        cube.position(0.5, 0.5, 0.0)
        cube.normal(0.408248, 0.816497, -0.408248)
        cube.textureCoord(0, 1)
        cube.position(-0.5, 0.5, 0.0)
        cube.normal(-0.666667, 0.333333, -0.666667)
        cube.textureCoord(1, 1)
        cube.position(0.5, 0.5, 1.0)
        cube.normal(0.666667, 0.333333, 0.666667)
        cube.textureCoord(0, 0)

        cube.triangle(0, 1, 2)
        cube.triangle(3, 1, 0)

        cube.triangle(4, 5, 6)
        cube.triangle(4, 7, 5)

        cube.triangle(8, 9, 10)
        cube.triangle(10, 7, 8)

        cube.triangle(4, 11, 12)
        cube.triangle(4, 13, 11)

        cube.triangle(14, 8, 12)
        cube.triangle(14, 15, 8)

        cube.triangle(16, 17, 18)
        cube.triangle(16, 19, 17)

        cube.end()

        return cube
