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
        sm = args['senemanager']
        randomnum = str(random.random())
        cube = sm.createEntity(randomnum, 'cube.mesh')
        cube.setMaterialName(self.texture)
        node = sm.getRootSceneNode().createChildSceneNode(randomnum + "_node", ogre.Vector3(self.x, self.y, self.z))
        node.attachObject(cube)

    def __str__(self):
        return "Block: %s is at (%i, %i, %i)" % (self.__class__.__name__, self.x, self.y, self.z)
