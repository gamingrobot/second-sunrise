from panda3d.core import Vec3, Point3, Quat, BitMask32
from panda3d.bullet import BulletCapsuleShape, BulletBoxShape, BulletRigidBodyNode

import math


# Config
G = 10.                       # gravitational constant
M = 1000.                    # mass of earth
m = 10.                       # mass of satelite
R = 25.                      # radius of orbit
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
        self.playernp.node().setLinearVelocity(Vec3(vR, 0, -v1))
        self.playernp.setPos(R, R, 0)
        self.playernp.node().setDeactivationEnabled(False)
        manager.physics.getWorld().attachRigidBody(self.playernp.node())

        manager.physics.registerPreFunc("playerController", self.update)
        manager.physics.registerPostFunc("playerController", self.postUpdate)

        manager.controls.registerKeyAll("Forward", "w", self.forward, self)

        self.lastrot = 0.0

    def start(self):
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

    def forward(self):
        log.debug("before", self.playernp.getH())
        self.playernp.setH(self.playernp.getH() + 10.0)
        log.debug("after", self.playernp.getH())
