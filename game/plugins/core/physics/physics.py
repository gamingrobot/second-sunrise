from panda3d.core import Vec3
from direct.showbase import DirectObject


#bullet includes
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape


class Physics(DirectObject.DirectObject):
    """SPAAAAAAAAAAAAAAAAAAAAAAAACE"""
    def __init__(self, xml):
        #init pre and post callbacks
        self.prePhysics = {}
        self.postPhysics = {}

        #bullet debug node
        debugNode = BulletDebugNode('Debug')
        debugNode.showWireframe(True)
        debugNode.showConstraints(True)
        debugNode.showBoundingBoxes(False)
        debugNode.showNormals(True)
        debugNP = render.attachNewNode(debugNode)
        debugNP.show()

        #create bullet world
        self.bulletworld = BulletWorld()
        self.bulletworld.setDebugNode(debugNP.node())
        self.bulletworld.setGravity(Vec3(0, 0, 0))

        #test colision
        shape2 = BulletSphereShape(20)
        self.earthnode = BulletRigidBodyNode('Earth')
        self.earthnode.setMass(1000000000000000000000000000000.0)
        self.earthnode.addShape(shape2)
        self.earthnode.setDeactivationEnabled(False)
        self.earthnp = render.attachNewNode(self.earthnode)
        self.earthnp.setPos(0, 0, 0)
        self.bulletworld.attachRigidBody(self.earthnode)

        #start doing physics
        self.physicsTask = taskMgr.add(self.simulationTask, 'Physics Loop', sort=100)

    def reload(self, xml):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def destroy(self):
        taskMgr.remove(self.physicsTask)
        del self.physicsTask

    def simulationTask(self, task):
        # Call the pre-physics functions
        for ident, func in self.prePhysics.iteritems():
            func()

        dt = globalClock.getDt()
        self.bulletworld.doPhysics(dt, 10, 1.0 / 180.0)

        # Call the post-physics functions
        for ident, func in self.postPhysics.iteritems():
            func()

        return task.cont

    def getWorld(self):
        return self.bulletworld

    def registerPreFunc(self, name, func):
        self.prePhysics[name] = func

    def unRegisterPreFunc(self, name):
        if name in self.prePhysics:
            del self.prePhysics[name]

    def registerPostFunc(self, name, func):
        self.postPhysics[name] = func

    def unRegisterPostFunc(self, name):
        if name in self.postPhysics:
            del self.postPhysics[name]
