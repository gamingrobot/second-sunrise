#bullet physics engine hello world with Panda3D
from pandac.PandaModules import loadPrcFileData

loadPrcFileData("", "show-frame-rate-meter #t")

#from direct.directbase.DirectStart import *
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import ZUp
from direct.showbase.InputStateGlobal import inputState
import math

#G = 0.981
G = 6.673 * 10 ** -11
#G = .5


class BulletTest(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        debugNode = BulletDebugNode('Debug')
        debugNode.showWireframe(True)
        debugNode.showConstraints(True)
        debugNode.showBoundingBoxes(False)
        debugNode.showNormals(True)
        debugNP = self.render.attachNewNode(debugNode)
        debugNP.show()

        # World
        self.world = BulletWorld()
        self.world.setDebugNode(debugNP.node())

        #movement setup
        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('left', 'a')
        inputState.watchWithModifiers('reverse', 's')
        inputState.watchWithModifiers('right', 'd')
        inputState.watchWithModifiers('turnLeft', 'q')
        inputState.watchWithModifiers('turnRight', 'e')

        #player
        h = 1.75
        w = 0.4
        shape = BulletCapsuleShape(w, h - 2 * w, ZUp)
        self.moonnode = BulletRigidBodyNode('Player')
        self.moonnode.setMass(1)
        self.moonnode.addShape(shape)
        self.moonnp = self.render.attachNewNode(self.moonnode)
        self.moonnp.setPos(-10, 25, 10)
        self.world.attachRigidBody(self.moonnode)
        self.moonmodel = self.loader.loadModel('models/box.egg')
        self.moonmodel.flattenLight()
        self.moonmodel.reparentTo(self.moonnp)
        self.moonmodel.setPos(-0.5, -0.5, -0.5)

        shape2 = BulletSphereShape(10)
        self.earthnode = BulletRigidBodyNode('Earth')
        self.earthnode.setMass(100000000000000)
        #self.earthnode.setMass(1000000000000000)
        #self.earthnode.setMass(1000)
        self.earthnode.addShape(shape2)
        self.earthnp = self.render.attachNewNode(self.earthnode)
        self.earthnp.setPos(0, 0, 0)
        self.world.attachRigidBody(self.earthnode)
        #self.earthmodel = self.loader.loadModel('models/box.egg')
        #self.earthmodel.flattenLight()
        #self.earthmodel.reparentTo(self.earthnp)
        #self.earthmodel.setPos(0, 0, 0)
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

        d = math.sqrt(difx ** 2 + dify ** 2 + difz ** 2)
        f = (G * moonmass * earthmass) / d ** 2

        fx = ((f / d) * difx) * -1
        fy = ((f / d) * dify) * -1
        fz = ((f / d) * difz) * -1

        th = 1
        if math.fabs(difx) <= th and math.fabs(dify) <= th and math.fabs(difz) <= th:
            #fx, fy, fz = 0, 0, 0
            self.moonnode.setLinearVelocity(Vec3(0, 0, 0))
        else:
            self.moonnode.applyForce(Vec3(fx, fy, fz), False)

        #player movement
        speed = self.moonnode.getLinearVelocity()
        omega = self.moonnode.getAngularVelocity()
        move = 0.1

        if inputState.isSet('forward'):
            speed.setY(speed.getY() + move)
        if inputState.isSet('reverse'):
            speed.setY(speed.getY() + move * -1)
        if inputState.isSet('left'):
            speed.setX(speed.getX() + move * -1)
        if inputState.isSet('right'):
            speed.setX(speed.getX() + move)
        if inputState.isSet('turnLeft'):
            omega = 10.0
        if inputState.isSet('turnRight'):
            omega = -10.0

        self.moonnode.setAngularVelocity(omega)
        self.moonnode.setLinearVelocity(speed)

        dt = globalClock.getDt()
        self.world.doPhysics(dt, 10, 1.0 / 60.0)
        return task.cont

app = BulletTest()
app.run()
