#Player
import sys
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
from panda3d.core import Vec3
import math
sys.path.insert(0, '..')
from MovableEntity import *
from Controls import *


class Player(MovableEntity):
    """Player"""
    def __init__(self, args):
        MovableEntity.__init__(self, args)
        self.root = args['root']
        #setup camera
        self.root.camera.setPos(args['x'], args['y'], args['z'])
        #create player mesh
        """shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        self.bplayer = BulletRigidBodyNode('Player')
        self.bplayer.setMass(1)
        self.bplayer.addShape(shape)
        self.player = self.root.render.attachNewNode(self.bplayer)
        self.player.setPos(args['x'], args['y'], args['z'])
        self.root.bulletworld.attachRigidBody(self.bplayer)
        model = self.root.loader.loadModel('models/box.egg')
        model.flattenLight()
        model.reparentTo(self.player)
        model.setPos(-0.5, -0.5, -0.5)"""
        #reparent player to camera
        #self.root.camera.reparentTo(self.player)
        #start the controller
        self.cont = Controls(args['root'])
        self.cont.gameMode()

    def __str__(self):
        return "A Player"

    def getPos(self):
        return self.player.getPos()

    def setPos(self, newpos):
        self.root.camera.setPos(newpos)

    def getMass(self):
        return self.bplayer.getMass()

    def applyForce(self, force, mode):
        self.bplayer.applyForce(force, mode)

    def setLinearVelocity(force):
        self.player.setLinearVelocity(force)
