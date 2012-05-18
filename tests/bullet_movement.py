from pandac.PandaModules import loadPrcFileData

#loadPrcFileData("", "sync-video #f")
loadPrcFileData("", "show-frame-rate-meter #t")

import sys
import direct.directbase.DirectStart

from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState


from panda3d.core import Vec3
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import ZUp


class Game(DirectObject):

    def __init__(self):
        base.cam.setPos(0, -20, 4)
        base.cam.lookAt(0, 0, 0)

        self.accept('f3', self.toggleDebug)

        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('left', 'a')
        inputState.watchWithModifiers('reverse', 's')
        inputState.watchWithModifiers('right', 'd')
        inputState.watchWithModifiers('turnLeft', 'q')
        inputState.watchWithModifiers('turnRight', 'e')

        # Task
        taskMgr.add(self.update, 'updateWorld')

        # Physics
        self.setup()

    def toggleDebug(self):
        if self.debugNP.isHidden():
            self.debugNP.show()
        else:
            self.debugNP.hide()

    def processInput(self):     # @IndentOk
        speed = Vec3(0, 0, 0)
        omega = 0.0

        if inputState.isSet('forward'):
                speed.setY(3.0)
        if inputState.isSet('reverse'):
                speed.setY(-3.0)
        if inputState.isSet('left'):
                speed.setX(-3.0)
        if inputState.isSet('right'):
                speed.setX(3.0)
        if inputState.isSet('turnLeft'):
                omega = 120.0
        if inputState.isSet('turnRight'):
                omega = -120.0

        self.player.setAngularMovement(omega)
        self.player.setLinearMovement(speed, True)

    def update(self, task):
        dt = globalClock.getDt()
        self.processInput()
        pos = self.playerNP.getPos()
        self.world.doPhysics(dt, 10, 0.008)
        pos2 = self.playerNP.getPos()
        distx = pos2[0] - pos[0]
        disty = pos2[1] - pos[1]
        print distx, disty

        return task.cont

    def setup(self):
        self.worldNP = render.attachNewNode('World')

        # World
        self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
        self.debugNP.show()

        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.world.setDebugNode(self.debugNP.node())

        # Ground
        shape = BulletPlaneShape(Vec3(0, 0, 1), 0)

        np = self.worldNP.attachNewNode(BulletRigidBodyNode('Ground'))
        np.node().addShape(shape)
        np.setPos(0, 0, -1)

        self.world.attachRigidBody(np.node())

        # Character
        self.crouching = False

        h = 1.75
        w = 0.4
        shape = BulletCapsuleShape(w, h - 2 * w, ZUp)

        node = BulletCharacterControllerNode(shape, 0.4, 'Player')
        np = self.worldNP.attachNewNode(node)
        np.setPos(-2, 0, 14)
        np.setH(45)

        self.world.attachCharacter(np.node())

        self.player = node      # For player control
        self.playerNP = np

game = Game()
run()
