#Player
import sys
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
from panda3d.core import Vec3
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import CollisionRay,CollisionNode,GeomNode,CollisionTraverser
from panda3d.core import CollisionHandlerQueue, CollisionSphere, BitMask32
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
        #setup picking
        #add mouse button 1 handler
        self.root.accept('mouse1', self.onMouseTask)
        #add mouse collision to our world
        self.setupMouseCollision()

    def __str__(self):
        return "A Player"

    def onMouseTask(self):
        """ """
        #do we have a mouse
        if (self.root.mouseWatcherNode.hasMouse() == False):
            return

        #get the mouse position
        mpos = base.mouseWatcherNode.getMouse()

        #Set the position of the ray based on the mouse position

        self.mPickRay.setFromLens(self.root.camNode, mpos.getX(), mpos.getY())

        #for this small example I will traverse everything, for bigger projects
        #this is probably a bad idea
        self.mPickerTraverser.traverse(self.root.render)

        if (self.mCollisionQue.getNumEntries() > 0):
            self.mCollisionQue.sortEntries()
            entry = self.mCollisionQue.getEntry(0)
            chunk = entry.getIntoNodePath()

            chunk = chunk.findNetTag('Pickable')
            if not chunk.isEmpty():
                #here is how you get the surface collsion
                block = entry.getSurfacePoint(self.root.render)
                print chunk.getName()
                print block
                #handleBlockClick(chunk, block)

    def setupMouseCollision(self):
        """ """
        #Since we are using collision detection to do picking, we set it up
        #any other collision detection system with a traverser and a handler
        self.mPickerTraverser = CollisionTraverser()  # Make a traverser
        self.mCollisionQue = CollisionHandlerQueue()

        #create a collision solid ray to detect against
        self.mPickRay = CollisionRay()
        self.mPickRay.setOrigin(self.root.camera.getPos(self.root.render))
        self.mPickRay.setDirection(render.getRelativeVector(camera, Vec3(0, 1, 0)))

        #create our collison Node to hold the ray
        self.mPickNode = CollisionNode('pickRay')
        self.mPickNode.addSolid(self.mPickRay)

        #Attach that node to the camera since the ray will need to be positioned
        #relative to it, returns a new nodepath
        #well use the default geometry mask
        #this is inefficent but its for mouse picking only

        self.mPickNP = self.root.camera.attachNewNode(self.mPickNode)

        #well use what panda calls the "from" node.  This is reall a silly convention
        #but from nodes are nodes that are active, while into nodes are usually passive environments
        #this isnt a hard rule, but following it usually reduces processing

        #Everything to be picked will use bit 1. This way if we were doing other
        #collision we could seperate it, we use bitmasks to determine what we check other objects against
        #if they dont have a bitmask for bit 1 well skip them!
        self.mPickNode.setFromCollideMask(GeomNode.getDefaultCollideMask())

        #Register the ray as something that can cause collisions
        self.mPickerTraverser.addCollider(self.mPickNP, self.mCollisionQue)
        #if you want to show collisions for debugging turn this on
        #self.mPickerTraverser.showCollisions(self.render)

    def getPos(self):
        return self.player.getPos()

    def setPos(self, newpos):
        self.root.camera.setPos(newpos)

    def getMass(self):
        return self.bplayer.getMass()

    def applyForce(self, force, mode):
        self.bplayer.applyForce(force, mode)

    def setLinearVelocity(self, force):
        self.player.setLinearVelocity(force)

    def lookAt(self, planet):
        self.root.camera.headsUp(planet)
