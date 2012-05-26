#CameraTest.py
from direct.task import Task
from panda3d.core import WindowProperties
from direct.showbase.InputStateGlobal import inputState
from math import *
from Menus import *
import sys


class Controls:
    def __init__(self, superapp):
        self.app = superapp
        self.overlay = OverlayMenu(self)
        #uncomment out below once the Play Game button works
        #self.mainmenu = MainMenu()
        self.ovrlay = False
        self.inGame = False
        #camera stuff
        self.app.disableMouse()
        self.app.accept("q", self.stop)
        self.app.accept("escape", self.toggleOverlay)

        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('left', 'a')
        inputState.watchWithModifiers('reverse', 's')
        inputState.watchWithModifiers('right', 'd')
        inputState.watchWithModifiers('crouch', 'shift')
        inputState.watchWithModifiers('jump', 'space')

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
        self.speed = .1

    def menuMode(self):
        #show mouse
        props = WindowProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        #set menu bool
        self.inGame = False
        taskMgr.remove('look')
        taskMgr.remove('move')

    def gameMode(self):
        #hide mouse
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)
        #set game bool
        self.inGame = True
        self.startLook()
        self.startMove()

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

    def startMove(self):
        taskMgr.add(self.move, 'move')

    def move(self, task):
        if inputState.isSet('forward'):
            dir = self.app.camera.getNetTransform().getMat().getRow3(1)
            dir.setZ(0)
            dir.normalize()
            self.pos += dir * self.speed
            self.app.camera.setPos(self.pos)
        if inputState.isSet('reverse'):
            dir = self.app.camera.getNetTransform().getMat().getRow3(1)
            dir.setZ(0)
            dir.normalize()
            self.pos -= dir * self.speed
            self.app.camera.setPos(self.pos)
        if inputState.isSet('left'):
            dir = self.app.camera.getNetTransform().getMat().getRow3(0)
            dir.setZ(0)
            dir.normalize()
            self.pos -= dir * self.speed
            self.app.camera.setPos(self.pos)
        if inputState.isSet('right'):
            dir = self.app.camera.getNetTransform().getMat().getRow3(0)
            dir.setZ(0)
            dir.normalize()
            self.pos += dir * self.speed
            self.app.camera.setPos(self.pos)
        if inputState.isSet('crouch'):
            dir = self.app.camera.getNetTransform().getMat().getRow3(2)
            #dir.setZ(0)
            dir.normalize()
            self.pos -= dir * self.speed
            self.app.camera.setPos(self.pos)
        if inputState.isSet('jump'):
            dir = self.app.camera.getNetTransform().getMat().getRow3(2)
            #dir.setZ(0)
            dir.normalize()
            self.pos += dir * self.speed
            self.app.camera.setPos(self.pos)
        return Task.cont

    def stop(self):
        taskMgr.remove('look')
        taskMgr.remove('move')
        self.app.stop()
        sys.exit()

    def toggleOverlay(self):
        self.ovrlay = not self.ovrlay

        if (self.ovrlay):
            self.overlay.show()
            self.menuMode()
        else:
            self.overlay.hide()
            self.gameMode()
