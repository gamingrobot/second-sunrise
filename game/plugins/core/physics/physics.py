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
        self.bulletworld.setGravity(Vec3(0, 0, -9.8))

        #test colision
        shape2 = BulletSphereShape(64)
        self.earthnode = BulletRigidBodyNode('Earth')
        self.earthnode.addShape(shape2)
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
        dt = globalClock.getDt()
        self.bulletworld.doPhysics(dt, 10, 1.0 / 180.0)
        return task.cont
