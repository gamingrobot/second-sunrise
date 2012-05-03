#bullet physics engine hello world with Panda3D

#from direct.directbase.DirectStart import *
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape


class BulletTest(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # World
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))

        # Plane
        shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
        node = BulletRigidBodyNode('Ground')
        node.addShape(shape)
        np = self.render.attachNewNode(node)
        np.setPos(0, 0, -2)
        self.world.attachRigidBody(node)

        # Box
        shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        node = BulletRigidBodyNode('Box')
        node.setMass(1.0)
        node.addShape(shape)
        np = self.render.attachNewNode(node)
        np.setPos(0, 0, 2)
        self.world.attachRigidBody(node)
        self.model = self.loader.loadModel('models/box.egg')
        self.model.flattenLight()
        self.model.reparentTo(np)
        self.model.setPos(-8, 42, 0)

        self.taskMgr.add(self.update, 'update')

    # Update
    def update(self, task):
        dt = globalClock.getDt()
        self.world.doPhysics(dt)
        return task.cont

app = BulletTest()
app.run()
