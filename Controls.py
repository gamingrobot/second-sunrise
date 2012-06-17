#CameraTest.py
from direct.task import Task
from panda3d.core import WindowProperties
from direct.showbase.InputStateGlobal import inputState
from math import *
import sys


class Controls:
    def __init__(self, root, player):

        #TODO: fix to be root
        self.root = root
        self.player = player

        self.inGame = False
        #camera stuff

        self.root.disableMouse()
        self.root.accept("escape", self.player.toggleInGameMenu)
        self.root.accept("q", self.stop)

        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('left', 'a')
        inputState.watchWithModifiers('reverse', 's')
        inputState.watchWithModifiers('right', 'd')
        inputState.watchWithModifiers('crouch', 'shift')
        inputState.watchWithModifiers('jump', 'space')

        #register stuff
        self.mouseChangeX = 0
        self.mouseChangeY = 0
        self.windowSizeX = self.root.win.getXSize()
        self.windowSizeY = self.root.win.getYSize()
        self.centerX = self.windowSizeX / 2
        self.centerY = self.windowSizeY / 2
        self.H = self.root.camera.getH()
        self.P = self.root.camera.getP()
        self.pos = self.root.camera.getPos()
        self.sensitivity = .05
        self.speed = .1

        self.gameMode()

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
        mouse = self.root.win.getPointer(0)
        x = mouse.getX()
        y = mouse.getY()
        if self.root.win.movePointer(0, self.centerX, self.centerY):
            self.mouseChangeX = self.centerX - x
            self.mouseChangeY = self.centerY - y
            self.H += self.mouseChangeX * self.sensitivity
            self.P += self.mouseChangeY * self.sensitivity
            self.root.camera.setHpr(self.H, self.P, 0)
            print "H" + str(self.H)
            #print "P" + str(self.P)
        return Task.cont

    def startLook(self):
        self.root.win.movePointer(0, self.centerX, self.centerY)
        taskMgr.add(self.look, 'look')

    def startMove(self):
        taskMgr.add(self.move, 'move')

    def move(self, task):
        self.H = self.root.camera.getH()
        self.P = self.root.camera.getP()
        self.pos = self.root.camera.getPos()
        if inputState.isSet('forward'):
            dir = self.root.camera.getNetTransform().getMat().getRow3(1)
            dir.setZ(0)
            dir.normalize()
            self.pos += dir * self.speed
            self.root.camera.setPos(self.pos)
        if inputState.isSet('reverse'):
            dir = self.root.camera.getNetTransform().getMat().getRow3(1)
            dir.setZ(0)
            dir.normalize()
            self.pos -= dir * self.speed
            self.root.camera.setPos(self.pos)
        if inputState.isSet('left'):
            dir = self.root.camera.getNetTransform().getMat().getRow3(0)
            dir.setZ(0)
            dir.normalize()
            self.pos -= dir * self.speed
            self.root.camera.setPos(self.pos)
        if inputState.isSet('right'):
            dir = self.root.camera.getNetTransform().getMat().getRow3(0)
            dir.setZ(0)
            dir.normalize()
            self.pos += dir * self.speed
            self.root.camera.setPos(self.pos)
        if inputState.isSet('crouch'):
            dir = self.root.camera.getNetTransform().getMat().getRow3(2)
            #dir.setZ(0)
            dir.normalize()
            self.pos -= dir * self.speed
            self.root.camera.setPos(self.pos)
        if inputState.isSet('jump'):
            dir = self.root.camera.getNetTransform().getMat().getRow3(2)
            #dir.setZ(0)
            dir.normalize()
            self.pos += dir * self.speed
            self.root.camera.setPos(self.pos)
        return Task.cont

    def stop(self):
        taskMgr.remove('look')
        taskMgr.remove('move')
        self.root.stop()
        sys.exit()
