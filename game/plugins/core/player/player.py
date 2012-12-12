from panda3d.core import Vec3, Point3, Quat, BitMask32
from panda3d.bullet import BulletCapsuleShape, BulletBoxShape, BulletRigidBodyNode
from direct.showbase.InputStateGlobal import inputState

import math


# Config
G = 10.                       # gravitational constant
M = 1000.                    # mass of earth
m = 10.                       # mass of satelite
R = 60.                      # radius of orbit
vR = 1.                      # initial radial velocity
f = 1.0                       # factor applied to orbital velocity

v1 = f * math.sqrt(G * M / R)     # orbital velocity, times factor


class Player:
    """A Player class - doesn't actually do that much, just arranges collision detection and provides a camera mount point, plus an interface for the controls to work with. All configured of course."""
    def __init__(self, xml):
        self.reload(xml)

    def reload(self, xml):
        self.playernp = render.attachNewNode(BulletRigidBodyNode('Player'))
        self.playernp.node().setMass(m)
        self.playernp.node().addShape(BulletBoxShape(Vec3(1, 1, 2)))
        #self.playernp.node().setLinearVelocity(Vec3(vR, 0, -v1))
        self.playernp.setPos(0, 0, R)
        self.playernp.node().setDeactivationEnabled(False)
        manager.physics.getWorld().attachRigidBody(self.playernp.node())

        manager.physics.registerPreFunc("playerController", self.update)
        manager.physics.registerPostFunc("playerController", self.postUpdate)

        #manager.controls.registerKeyAll("Forward", "w", self.forward, self)

        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('left', 'a')
        inputState.watchWithModifiers('reverse', 's')
        inputState.watchWithModifiers('right', 'd')
        inputState.watchWithModifiers('turnLeft', 'q')
        inputState.watchWithModifiers('turnRight', 'e')

        self.__currentPos = Vec3(0, 0, 0)

    def start(self):
        #events.triggerEvent("playerspawn", self.playernp.getPos())
        pass

    def stop(self):
        pass

    def destroy(self):
        pass

    def update(self):
        # Apply gravity
        gravity = Point3.zero() - self.playernp.getPos()
        gravity.normalize()
        gravity *= G * M * m / (R ** 2)
        self.playernp.node().applyCentralForce(gravity)

    def postUpdate(self):
        planet = Point3.zero()
        normal = Vec3(self.playernp.getX() - planet.getX(), self.playernp.getY() - planet.getY(), self.playernp.getZ() - planet.getZ())
        normal.normalize()
        fwd = render.getRelativePoint(self.playernp, Vec3(0, 1, 0))
        self.playernp.headsUp(fwd, normal)

        self.__currentPos = self.playernp.getPos()

        #player movement
        #space physcis
        #speed = self.playernp.node().getLinearVelocity()
        #normal physcis
        speed = Vec3(0, 0, 0)
        omega = 0.0
        v = 5.8
        if inputState.isSet('forward'): speed.setY(v)
        if inputState.isSet('reverse'): speed.setY(-v)
        if inputState.isSet('left'):    speed.setX(-v)
        if inputState.isSet('right'):   speed.setX(v)

        if inputState.isSet('flyUp'):   speed.setZ( 2.0)
        if inputState.isSet('flyDown'):   speed.setZ( -2.0)

        if inputState.isSet('turnLeft'):  omega =  40.0
        if inputState.isSet('turnRight'): omega = -40.0

        self.playernp.setH(self.playernp, omega * globalClock.getDt())

        globalVel = self.playernp.getQuat(render).xform(speed) * globalClock.getDt()

        normalVel = Vec3(globalVel)
        normalVel.normalize()

        if globalVel != Vec3():
            globalVelDir = Vec3(globalVel)
            globalVelDir.normalize()

            fn = Vec3(0.0, 0.0, 0.0)
            fn.normalize()

            velDot = 1.0 - globalVelDir.angleDeg(fn) / 180.0
            if velDot < 0.5:
                self.__currentPos -= Vec3(fn.x * globalVel.x, fn.y * globalVel.y, globalVel.z * globalVel.y) * velDot

            globalVel *= velDot

        self.__currentPos += globalVel

        self.playernp.setPos(self.__currentPos)

        #fix so its not called so often
        #events.triggerEvent("playermove", self.playernp.getPos())

    def forward(self):
        log.debug("before", self.playernp.getH())
        self.playernp.setH(self.playernp.getH() + 10.0)
        log.debug("after", self.playernp.getH())
