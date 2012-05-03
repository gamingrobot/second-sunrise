#bullet physics engine hello world with Panda3D

#from direct.directbase.DirectStart import *
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
import math

zero_vector = [0.0, 0.0, 0.0]
G = 0.981


class BulletTest(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.gravity_point = zero_vector

        # World
        self.world = BulletWorld()
        #self.world.setGravity(Vec3(0,0,0))

        # Plane
        #shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
        #node = BulletRigidBodyNode('Ground')
        #node.addShape(shape)
        #np = self.render.attachNewNode(node)
        #np.setPos(0, 0, -2)
        #self.world.attachRigidBody(node)

        # Box
        shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        self.node = BulletRigidBodyNode('Box')
        self.node.setMass(0.01)
        self.node.addShape(shape)
        self.np = self.render.attachNewNode(self.node)
        self.np.setPos(0, 0, 2)
        self.world.attachRigidBody(self.node)
        self.model = self.loader.loadModel('models/box.egg')
        self.model.flattenLight()
        self.model.reparentTo(self.np)
        self.model.setPos(10, 50, -10)

        """self.node2 = BulletRigidBodyNode('Box')
        self.node2.setMass(1.0)
        self.node2.addShape(shape)
        self.np2 = self.render.attachNewNode(self.node2)
        self.np2.setPos(0, 0, 2)
        self.world.attachRigidBody(self.node2)
        self.model2 = self.loader.loadModel('models/box.egg')
        self.model2.flattenLight()
        self.model2.reparentTo(self.np2)
        self.model2.setPos(0, 0, 0)"""

        self.taskMgr.add(self.update, 'update')

    # Update
    def update(self, task):
        pos = self.np.getPos()
        gv = [self.gravity_point[0] - pos[0], self.gravity_point[1] - pos[1], self.gravity_point[2] - pos[2]]
        d = math.sqrt((gv[0] * gv[0]) + (gv[1] * gv[1]) + (gv[2] * gv[2]))
        f = G * self.node.getMass()/(d*d)
        gv = [(f/d)*gv[0],(f/d)*gv[1],(f/d)*gv[2]]
        print gv
        self.node.applyForce(Vec3(gv[1], gv[1], gv[2]), False)

        """pos = self.np2.getPos()
        gv = [self.gravity_point[0] - pos[0], self.gravity_point[1] - pos[1], self.gravity_point[2] - pos[2]]
        d = math.sqrt((gv[0] * gv[0]) + (gv[1] * gv[1]) + (gv[2] * gv[2]))
        f = G * self.node2.getMass()/(d*d)
        gv = [(f/d)*gv[0],(f/d)*gv[1],(f/d)*gv[2]]
        print gv
        self.node2.applyForce(Vec3(gv[0], gv[1], gv[2]), False)"""

        dt = globalClock.getDt()
        self.world.doPhysics(dt)
        return task.cont

app = BulletTest()
app.run()
