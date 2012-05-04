#CameraTest.py
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile
from panda3d.core import Vec3
from direct.task import Task
from math import *
import sys

loadPrcFile("config/Config.prc")


class CameraTest(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        temp = self.loader.loadModel("models/box")
        temp.reparentTo(self.render)
        temp.setPos(0, 20, 0)
        #camera stuff
        self.disableMouse()
        self.camera.lookAt(temp)

        #register events
        self.accept("w", self.walkForward)
        self.accept("w-up", self.walkForward)
        self.accept("escape", sys.exitfunc)

        #register stuff
        self.mouseChangeX = 0
        self.mouseChangeY = 0
        self.windowSizeX = self.win.getXSize()
        self.windowSizeY = self.win.getYSize()
        self.centerX = self.windowSizeX / 2
        self.centerY = self.windowSizeY / 2
        self.H = self.camera.getH()
        self.P = self.camera.getP()
        self.pos = self.camera.getPos()
        self.sensitivity = .05
        self.speed = .01
        self.isWalking = False
        self.startMovement()

    def movement(self, task):
        mouse = self.win.getPointer(0)
        x = mouse.getX()
        y = mouse.getY()
        if self.win.movePointer(0, self.centerX, self.centerY):
            self.mouseChangeX = self.centerX - x
            self.mouseChangeY = self.centerY - y
            self.H += self.mouseChangeX * self.sensitivity
            self.P += self.mouseChangeY * self.sensitivity
            self.camera.setHpr(self.H, self.P, 0)
        return Task.cont

    def startMovement(self):
        self.win.movePointer(0, self.centerX, self.centerY)
        taskMgr.add(self.movement, 'movement')

    def stopMovement(self):
        taskMgr.remove('movement')

    def walkForward(self):
        if self.isWalking:
            self.isWalking = False
            taskMgr.remove('moveForward')
        else:
            self.isWalking = True
            taskMgr.add(self.walk, 'moveForward')

    def walk(self, task):
        dir = self.camera.getNetTransform().getMat().getRow3(1)
        dir.setZ(0)
        dir.normalize()
        self.pos += dir * self.speed
        self.camera.setPos(self.pos)
        return Task.cont

app = CameraTest()
app.run()
