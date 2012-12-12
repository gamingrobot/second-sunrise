from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletGhostNode, BulletRigidBodyNode


class Planet:
    """Planet"""
    def __init__(self, cords, radius, name, parentnode):
        self.cords = cords
        self.planetNode = parentnode.attachNewNode(name)
        self.planetNode.setPos(cords)
        self.psize = radius  # chunks
        self.radius = (self.psize / 2)

        #planet
        self.colisionnp = parentnode.attachNewNode(BulletGhostNode(name))
        self.colisionnp.node().addShape(BulletSphereShape(radius * 16))
        self.colisionnp.setPos(0, 0, 0)
        self.colisionnp.node().setDeactivationEnabled(False)
        manager.physics.getWorld().attachGhost(self.colisionnp.node())
        """
        self.colisionnp = parentnode.attachNewNode(BulletRigidBodyNode(name))
        self.colisionnp.node().addShape(BulletSphereShape(radius * 16))
        self.colisionnp.setPos(0, 0, 0)
        self.colisionnp.node().setDeactivationEnabled(False)
        manager.physics.getWorld().attachRigidBody(self.colisionnp.node())"""

    def getNode(self):
        return self.planetNode
