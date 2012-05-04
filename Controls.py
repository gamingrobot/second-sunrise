#CameraTest.py
from direct.task import Task
from math import *


class Controls:
    def __init__(self, superapp, noclip):
        self.app = superapp
        #camera stuff
        self.app.disableMouse()

        #register events
        self.app.accept("w", self.walkForward)
        self.app.accept("w-up", self.walkForward)
        self.app.accept("s", self.walkBack)
        self.app.accept("s-up", self.walkBack)
        self.app.accept("a", self.walkLeft)
        self.app.accept("a-up", self.walkLeft)
        self.app.accept("d", self.walkRight)
        self.app.accept("d-up", self.walkRight)
        self.app.accept("space", self.jump)
        self.app.accept("space-up", self.jump)
        self.app.accept("escape", self.stop)

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
        self.isWalkingF = False
        self.isWalkingB = False
        self.isWalkingL = False
        self.isWalkingR = False
        self.isJumping = False
        self.startLook()

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
        self.app.exitfunc()

    def walkForward(self):
        if self.isWalkingF:
            self.isWalkingF = False
            taskMgr.remove('walkForward')
        else:
            self.isWalkingF = True
            taskMgr.add(self.walkForwardTask, 'walkForward')

    def walkForwardTask(self, task):
        dir = self.app.camera.getNetTransform().getMat().getRow3(1)
        dir.setZ(0)
        dir.normalize()
        self.pos += dir * self.speed
        self.app.camera.setPos(self.pos)
        return Task.cont

    def walkBack(self):
        if self.isWalkingB:
            self.isWalkingB = False
            taskMgr.remove('walkBack')
        else:
            self.isWalkingB = True
            taskMgr.add(self.walkBackTask, 'walkBack')

    def walkBackTask(self, task):
        dir = self.app.camera.getNetTransform().getMat().getRow3(1)
        dir.setZ(0)
        dir.normalize()
        self.pos -= dir * self.speed
        self.app.camera.setPos(self.pos)
        return Task.cont

    def walkLeft(self):
        if self.isWalkingL:
            self.isWalkingL = False
            taskMgr.remove('walkLeft')
        else:
            self.isWalkingL = True
            taskMgr.add(self.walkLeftTask, 'walkLeft')

    def walkLeftTask(self, task):
        dir = self.app.camera.getNetTransform().getMat().getRow3(0)
        dir.setZ(0)
        dir.normalize()
        self.pos -= dir * self.speed
        self.app.camera.setPos(self.pos)
        return Task.cont

    def walkRight(self):
        if self.isWalkingR:
            self.isWalkingR = False
            taskMgr.remove('walkRight')
        else:
            self.isWalkingR = True
            taskMgr.add(self.walkRightTask, 'walkRight')

    def walkRightTask(self, task):
        dir = self.app.camera.getNetTransform().getMat().getRow3(0)
        dir.setZ(0)
        dir.normalize()
        self.pos += dir * self.speed
        self.app.camera.setPos(self.pos)
        return Task.cont

    def jump(self):
        if self.isJumping:
            self.isJumping = False
            taskMgr.remove('jump')
        else:
            self.isJumping = True
            taskMgr.add(self.jumpTask, 'jump')

    def jumpTask(self, task):
        dir = self.app.camera.getNetTransform().getMat().getRow3(2)
        print dir
        #dir.setZ(0)
        dir.normalize()
        self.pos += dir * self.speed
        self.app.camera.setPos(self.pos)
        return Task.cont
