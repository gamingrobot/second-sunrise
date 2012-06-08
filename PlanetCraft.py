#PlanetCraft.py
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile
from panda3d.core import PointLight
from panda3d.core import AmbientLight
from panda3d.core import VBase4
from panda3d.core import Point3
from panda3d.core import Vec3
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape

import math


#uncomment and run when you add a block, then re comment on next run
#import BlockIniter
#import EntityIniter
#BlockIniter.initBlocks()
#EntityIniter.initBlocks()

from Blocks import *
from Entities import *
#from Controls import *
#import shelve
#import numpy as np

loadPrcFile("config/Config.prc")


class PlanetCraft(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setBackgroundColor(0, 0, 0, 1)
        #bullet debug node
        debugNode = BulletDebugNode('Debug')
        debugNode.showWireframe(True)
        debugNode.showConstraints(True)
        debugNode.showBoundingBoxes(False)
        debugNode.showNormals(True)
        debugNP = self.render.attachNewNode(debugNode)
        debugNP.show()

        #create bullet world
        self.bulletworld = BulletWorld()
        self.bulletworld.setDebugNode(debugNP.node())

        #test colision
        shape2 = BulletSphereShape(64)
        self.earthnode = BulletRigidBodyNode('Earth')
        self.earthnode.addShape(shape2)
        self.earthnp = self.render.attachNewNode(self.earthnode)
        self.earthnp.setPos(0, 0, 0)
        self.bulletworld.attachRigidBody(self.earthnode)

        #model = self.loader.loadModel('models/box.egg')
        #model.reparentTo(self.render)
        #model.setPos(0, 0, 0)

        #create player
        self.player = Player({'x': -10, 'y': 25, 'z': 10, 'root': self})
        #create planet
        gamma = Planet({'x': 0, 'y': 0, 'z': 0, 'render': self.render, 'root': self})

        gamma.spawnPlayer(self.player)

        #gamma.testChunk()

        """plight = PointLight('plight')
        plight.setColor(VBase4(1, 1, 1, 1))
        #plight.setAttenuation(Point3(0, 0, 0.5))
        plnp = self.render.attachNewNode(plight)
        plnp.setPos(0, 0, 0)
        self.render.setLight(plnp)"""

        """alight = AmbientLight('alight')
        alight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)"""

        #centx, centy, centz = gamma.getCenter()
        #print str(centx) + str(centy) + str(centz)

        #do physics
        self.taskMgr.add(self.bulletupdate, 'bulletupdate')

    def bulletupdate(self, task):
        """ G = 6.673 * 10 ** -11
        playerpos = self.player.getPos()
        planetpos = (0, 0, 0)
        playermass = self.player.getMass()
        planetmass = 100000000000000

        #find chunk player is in

        difx = playerpos[0] - planetpos[0]
        dify = playerpos[1] - planetpos[1]
        difz = playerpos[2] - planetpos[2]

        d = math.sqrt(difx ** 2 + dify ** 2 + difz ** 2)
        f = (G * playermass * planetmass) / d ** 2

        fx = ((f / d) * difx) * -1
        fy = ((f / d) * dify) * -1
        fz = ((f / d) * difz) * -1

        th = 1
        if math.fabs(difx) <= th and math.fabs(dify) <= th and math.fabs(difz) <= th:
            #fx, fy, fz = 0, 0, 0
            self.player.setLinearVelocity(Vec3(0, 0, 0))
        else:
            self.player.applyForce(Vec3(fx, fy, fz), False)"""

        """#player movement
        speed = self.bplayer.getLinearVelocity()
        omega = self.bplayer.getAngularVelocity()
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

        self.bplayer.setAngularVelocity(omega)
        self.bplayer.setLinearVelocity(speed)"""

        dt = globalClock.getDt()
        self.bulletworld.doPhysics(dt, 10, 1.0 / 60.0)
        return task.cont

    def stop(self):
        pass


app = PlanetCraft()
app.run()
