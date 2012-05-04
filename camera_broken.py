#CameraTest.py
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile
from panda3d.core import Vec3
from math import *

loadPrcFile("config/Config.prc")


class CameraTest(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        temp = self.loader.loadModel("models/box")
        temp.reparentTo(self.render)
        temp.setPos(0, 0, 0)
        #camera stuff
        self.center = self.findCenter()
        #self.disableMouse()
        self.camera.setPos(0, 0, 0)
        self.accept("w", self.wPressed)
        self.mLastTime = 0.0
        self.taskMgr.add(self.mouseTask, 'updateCamera')

        self.mMotionGain = 1
        self.mHeadingGain = 5
        self.mPitchGain = 5
        self.mRollGain = 12
        self.mDriveDir = 0
        self.mLateralSlideDir = 0
        self.mVerticalSlideDir = 0

    def wPressed(self):
        print "wpressed"

    def findCenter(self):
        # Querry the screen size
        #   and calculate the center
        self.props = self.win.getProperties()
        self.winX = self.props.getXSize()
        self.winY = self.props.getYSize()
        return [self.winX / 2, self.winY / 2]

    def mouseTask(self, task):
        # Get time differential
        self.dt = globalClock.getFrameTime() - self.mLastTime
        self.mLastTime = globalClock.getFrameTime()

        # Get window size
        self.wp = self.win.getProperties()
        self.winWidth = self.wp.getXSize()
        self.winWidth2 = self.winWidth / 2
        self.winHeight = self.wp.getYSize()
        self.winHeight2 = self.winHeight / 2

        # Compute mapping from (0,W-1) onto (-W/2,W/2)
        self.xTrans = \
         self.ComputeMapping(\
            0.0, float(self.winWidth - 1), \
            -float(self.winWidth2), float(self.winWidth2) \
         )

        # Compute mapping from (0,H-1) onto (-H/2,H/2)
        self.yTrans = \
         self.ComputeMapping(\
            0.0, float(self.winHeight - 1), \
            -float(self.winHeight2), float(self.winHeight2) \
         )

        # Get cursor coordinates
        self.md = self.win.getPointer(0)
        self.cursorX = self.md.getX()
        self.cursorY = self.md.getY()

        # Convert using transform
        self.xCursor = self.xTrans[0] * float(self.cursorX) + self.xTrans[1]
        self.yCursor = self.yTrans[0] * float(self.cursorY) + self.yTrans[1]

        self.aButtonIsDown = False

        # Init delta angles
        self.dHeading = 0
        self.dPitch = 0
        self.dRoll = 0

        # Heading and pitch (mouse)
        #self.mouseButton0Down = self.mDevButtons[0].mIsPressed
        #if self.mouseButton0Down:
        #    self.delx = float(self.mCoordinates[0]) - self.xCursor
        #    self.dely = float(self.mCoordinates[1]) - self.yCursor

        self.delx = self.xCursor * self.dt
        self.dely = self.yCursor * self.dt

        self.sx = self.Sign(self.delx)
        self.sy = self.Sign(self.dely)

        self.dx = self.delx * self.delx * self.sx * self.mHeadingGain
        self.dy = self.dely * self.dely * self.sy * self.mPitchGain

        self.dHeading += -self.dx
        self.dPitch += self.dy
        self.aButtonIsDown = True

        # Roll
        """self.mouseButton2Down = self.mIsPressed
        if self.mouseButton2Down:
            self.delx = float(self.mCoordinates[0]) - self.xCursor
            # dely = float(self.mDevButtons[0].mCoordinates[1]) - yCursor

            self.delx = self.xCursor * self.dt
            # dely = yCursor*dt

            self.dir = Sign(self.delx)

            self.da = fabs(self.delx * self.delx) * self.dir * self.mRollGain
            self.dPitch += self.da

            self.aButtonIsDown = True
            """
        """# Get direction of travel
        self.mouseButton1Down = self.mIsPressed
        self.direction = 1
        if self.mouseButton1Down:
            self.aButtonIsDown = True
            self.direction = -1"""

        self.dPos = Vec3(0, 0, 0) * 1

        # Update camera
        if self.mDriveDir != 0:
            self.quat = self.camera.getQuat()
            self.fw = self.quat.getForward()
            self.cPos = self.camera.getPos()
            self.dPos = self.dPos + self.fw * self.mMotionGain * self.mDriveDir

        if self.mLateralSlideDir != 0:
            self.quat = self.camera.getQuat()
            self.rt = self.quat.getRight()
            self.cPos = self.camera.getPos()
            self.dPos = self.dPos + self.rt * self.mMotionGain * self.mLateralSlideDir

        if self.mVerticalSlideDir != 0:
            self.quat = self.camera.getQuat()
            self.up = self.quat.getUp()
            self.cPos = self.camera.getPos()
            self.dPos = self.dPos + self.up * self.mMotionGain * self.mVerticalSlideDir

        self.dPos = self.dPos * self.mMotionGain * self.dt
        self.cPos = self.camera.getPos() + self.dPos
        self.camera.setPos(self.cPos)

        self.dHpr = Vec3(self.dHeading, self.dPitch, self.dRoll) * self.dt
        self.cHpr = self.camera.getHpr() + self.dHpr
        self.camera.setHpr(self.cHpr)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #
    def getPos(self):
        return self.camera.getPos()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #
    def getHpr(self):
        return self.camera.getHpr()

    def ComputeMapping(self, a0, a1, b0, b1):
        if (a1 - a0) == 0:
            slope = 0
            intercept = 0
        else:
            slope = (b1 - b0) / (a1 - a0)
            intercept = b1 - slope * a1
        return [slope, intercept]

    def Sign(self, x):
        if x < 0:
            return -1
        return 1

app = CameraTest()
app.run()
