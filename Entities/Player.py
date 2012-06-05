#Player
import sys
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
from panda3d.core import Vec3
sys.path.insert(0, '..')
from MovableEntity import *
from Controls import *


class Player(MovableEntity):
    """Player"""
    def __init__(self, args):
        MovableEntity.__init__(self, args)
        self.root = args['root']
        #create player mesh
        shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        node = BulletRigidBodyNode('Player')
        node.setMass(1)
        node.addShape(shape)
        player = self.root.render.attachNewNode(node)
        player.setPos(args['x'], args['y'], args['z'])
        self.root.bulletworld.attachRigidBody(node)
        model = self.root.loader.loadModel('models/box.egg')
        model.flattenLight()
        model.reparentTo(player)
        model.setPos(-0.5, -0.5, -0.5)
        #reparent camera to player mesh
        self.root.camera.reparentTo(player)
        #start the controller
        self.cont = Controls(args['root'])
        self.cont.gameMode()

    def __str__(self):
        return "A Player"
