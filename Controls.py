#CameraTest.py
from direct.task import Task
from panda3d.core import WindowProperties
from math import *
import sys


class Controls:
    def __init__(self, superapp):
        self.app = superapp
        #camera stuff
        self.app.disableMouse()

    def menuMode(self):
        #show mouse
        props = WindowProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        #stop events
        taskMgr.remove('look')
        taskMgr.remove('walkForward')
        taskMgr.remove('walkBack')
        taskMgr.remove('walkLeft')
        taskMgr.remove('walkRight')
        taskMgr.remove('jump')
        taskMgr.remove('crouch')
        #fix registers
        self.app.accept("w", self.dummy)
        self.app.accept("w-up", self.dummy)
        self.app.accept("s", self.dummy)
        self.app.accept("s-up", self.dummy)
        self.app.accept("a", self.dummy)
        self.app.accept("a-up", self.dummy)
        self.app.accept("d", self.dummy)
        self.app.accept("d-up", self.dummy)
        self.app.accept("space", self.dummy)
        self.app.accept("space-up", self.dummy)
        self.app.accept("shift", self.dummy)
        self.app.accept("shift-up", self.dummy)
        self.app.accept("q", self.stop)
        self.app.accept("escape", self.app.overlay)

    def gameMode(self):
        #hide mouse
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)
        #register events
        self.app.accept("w", self.walkForward)
        self.app.accept("w-up", self.walkForwardUp)
        self.app.accept("s", self.walkBack)
        self.app.accept("s-up", self.walkBackUp)
        self.app.accept("a", self.walkLeft)
        self.app.accept("a-up", self.walkLeftUp)
        self.app.accept("d", self.walkRight)
        self.app.accept("d-up", self.walkRightUp)
        self.app.accept("space", self.jump)
        self.app.accept("space-up", self.jumpUp)
        self.app.accept("shift", self.crouch)
        self.app.accept("shift-up", self.crouchUp)
        self.app.accept("q", self.stop)
        self.app.accept("escape", self.app.overlay)

        #register stuff
        self.mouseChangeX = 0
        self.mouseChangeY = 0
        self.windowSizeX = self.app.win.getXSize()
        self.windowSizeY = self.app.win.getYSize()
        self.centerX = self.windowSizeX / 2
        self.centerY = self.windowSizeY / 2
        self.H = self.app.camera.getH()
        self.P = self.app.camera.getP()
        self.pos = self.app.camera.getPos()
        self.sensitivity = .05
        self.speed = .01
        self.startLook()

    def dummy(self):
        pass

    def look(self, task):
        mouse = self.app.win.getPointer(0)
        x = mouse.getX()
        y = mouse.getY()
        if self.app.win.movePointer(0, self.centerX, self.centerY):
            self.mouseChangeX = self.centerX - x
            self.mouseChangeY = self.centerY - y
            self.H += self.mouseChangeX * self.sensitivity
            self.P += self.mouseChangeY * self.sensitivity
            self.app.camera.setHpr(self.H, self.P, 0)
        return Task.cont

    def startLook(self):
        self.app.win.movePointer(0, self.centerX, self.centerY)
        taskMgr.add(self.look, 'look')

    def stop(self):
        taskMgr.remove('look')
        taskMgr.remove('walkForward')
        taskMgr.remove('walkBack')
        taskMgr.remove('walkLeft')
        taskMgr.remove('walkRight')
        taskMgr.remove('jump')
        taskMgr.remove('crouch')
        self.app.stop()
        sys.exit()

    def walkForward(self):
        taskMgr.add(self.walkForwardTask, 'walkForward')

    def walkForwardUp(self):
        taskMgr.remove('walkForward')

    def walkForwardTask(self, task):
        dir = self.app.camera.getNetTransform().getMat().getRow3(1)
        dir.setZ(0)
        dir.normalize()
        self.pos += dir * self.speed
        self.app.camera.setPos(self.pos)
        return Task.cont

    def walkBack(self):
        taskMgr.add(self.walkBackTask, 'walkBack')

    def walkBackUp(self):
        taskMgr.remove('walkBack')

    def walkBackTask(self, task):
        dir = self.app.camera.getNetTransform().getMat().getRow3(1)
        dir.setZ(0)
        dir.normalize()
        self.pos -= dir * self.speed
        self.app.camera.setPos(self.pos)
        return Task.cont

    def walkLeft(self):
        taskMgr.add(self.walkLeftTask, 'walkLeft')

    def walkLeftUp(self):
        taskMgr.remove('walkLeft')

    def walkLeftTask(self, task):
        dir = self.app.camera.getNetTransform().getMat().getRow3(0)
        dir.setZ(0)
        dir.normalize()
        self.pos -= dir * self.speed
        self.app.camera.setPos(self.pos)
        return Task.cont

    def walkRight(self):
        taskMgr.add(self.walkRightTask, 'walkRight')

    def walkRightUp(self):
        taskMgr.remove('walkRight')

    def walkRightTask(self, task):
        dir = self.app.camera.getNetTransform().getMat().getRow3(0)
        dir.setZ(0)
        dir.normalize()
        self.pos += dir * self.speed
        self.app.camera.setPos(self.pos)
        return Task.cont

    def jump(self):
        taskMgr.add(self.jumpTask, 'jump')

    def jumpUp(self):
        taskMgr.remove('jump')

    def jumpTask(self, task):
        dir = self.app.camera.getNetTransform().getMat().getRow3(2)
        #dir.setZ(0)
        dir.normalize()
        self.pos += dir * self.speed
        self.app.camera.setPos(self.pos)
        return Task.cont

    def crouch(self):
        taskMgr.add(self.crouchTask, 'crouch')

    def crouchUp(self):
        taskMgr.remove('crouch')

    def crouchTask(self, task):
        dir = self.app.camera.getNetTransform().getMat().getRow3(2)
        #dir.setZ(0)
        dir.normalize()
        self.pos -= dir * self.speed
        self.app.camera.setPos(self.pos)
        return Task.cont
