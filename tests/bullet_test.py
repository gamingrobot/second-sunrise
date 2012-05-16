#bullet physics engine hello world with Panda3D

#from direct.directbase.DirectStart import *
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
import math

zero_vector = [0.0, 0.0, 0.0]
#G = 0.981
G = 6.673 * 10 ** -11
#G = .5

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
        self.moonnode = BulletRigidBodyNode('Box')
        self.moonnode.setMass(1)
        self.moonnode.addShape(shape)
        self.moonnp = self.render.attachNewNode(self.moonnode)
        self.moonnp.setPos(-20, 20, -20)
        self.world.attachRigidBody(self.moonnode)
        self.moonmodel = self.loader.loadModel('models/box.egg')
        self.moonmodel.flattenLight()
        self.moonmodel.reparentTo(self.moonnp)
        self.moonmodel.setPos(0, 0, 0)

        shape2 = BulletSphereShape(10)
        self.earthnode = BulletRigidBodyNode('Box')
        self.earthnode.setMass(10000000000000)
        self.earthnode.addShape(shape2)
        self.earthnp = self.render.attachNewNode(self.earthnode)
        self.earthnp.setPos(0, 0, 0)
        self.world.attachRigidBody(self.earthnode)
        self.earthmodel = self.loader.loadModel('models/box.egg')
        self.earthmodel.flattenLight()
        self.earthmodel.reparentTo(self.earthnp)
        self.earthmodel.setPos(0, 0, 0)
        #self.earthmodel.setScale(10)

        self.taskMgr.add(self.update, 'update')

    # Update
    def update(self, task):
        moonpos = self.moonnp.getPos()
        earthpos = self.earthnp.getPos()
        moonmass = self.moonnode.getMass()
        earthmass = self.earthnode.getMass()

        difx = moonpos[0] - earthpos[0]
        dify = moonpos[1] - earthpos[1]
        difz = moonpos[2] - earthpos[2]

        ftop = G * earthmass * moonmass
        #prevent divide by 0
        if(difx == 0):
            fx = 0
        else:
            fx = ftop / difx ** 2
        if(dify == 0):
            fy = 0
        else:
            fy = ftop / dify ** 2
        if(difz == 0):
            fz = 0
        else:
            fz = ftop / difz ** 2

        #fix vector direction
        if fx > 0 and difx > 0:
            fx = fx * -1

        if fy > 0 and dify > 0:
            fy = fy * -1

        if fz > 0 and difz > 0:
            fz = fz * -1

        #print str(difx) + "," + str(dify) + "," + str(difz)

        #gv = [self.gravity_point[0] - pos[0], self.gravity_point[1] - pos[1], self.gravity_point[2] - pos[2]]
        #d = math.sqrt((gv[0] * gv[0]) + (gv[1] * gv[1]) + (gv[2] * gv[2]))
        #f = G * self.node.getMass()/(d*d)
        #gv = [(f/d)*gv[0],(f/d)*gv[1],(f/d)*gv[2]]
        #print gv

        self.moonnode.applyForce(Vec3(fx, fy, fz), False)

        print str(fx) + "," + str(fy) + "," + str(fz)

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
