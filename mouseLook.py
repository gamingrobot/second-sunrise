from panda3d.core import Vec3, Quat, Point3, WindowProperties, PythonTask
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import DirectObject


class MouseLook(DirectObject, object):

    MLMFPP = 0
    MLMOrbit = 1
    MLMPan = 2

    def __init__(self, targetCam=None, targetWin=None):
        self.setTargetCamera(targetCam)
        self.setTargetWin(targetWin)

        self.orbitCenter = Point3(0, 0, 0)

        self.mouseLookMode = self.MLMOrbit
        self.zoomOrtho = False
        self.centerMouse = False

        self.limitH = {
            "left": None,
            "right": None,
            "relative": render,
        }

        self.pause = False

        self.movementSpeed = 128.0
        self.wheelSpeed = 8.0
        self.mouseLookSpeed = [0.1, 0.1]

        self.camMove = dict(
            forward = False,
            backward = False,
            strafeLeft = False,
            strafeRight = False,
            down = False,
            up = False,
        )

    def zoom(self, direction):
        step = 64
        top = 32768
        bottom = 64

        fsH, size = self.lens.getFilmSize()
        size -= direction * step

        if size < bottom:
            size = bottom

        for vp in self.editorBase.viewports[1:4]:
            vp.zoomLocal(size)

    def zoomLocal(self, size):
        fsH = size * self.aspectRatio
        fsV = size
        self.lens.setFilmSize(fsH, fsV)

    #~ def pointAt(self, target, time):
        #~ Sequence(
            #~ Func(self.setPause, True),
            #~ CameraLookAtInterval(self.targetCamera, 0, time, target),
            #~ Func(self.setPause, False),
        #~ ).start()

    def enable(self, ownTask = True):
        self.prevX = self.targetWin.getPointer(0).getX()
        self.prevY = self.targetWin.getPointer(0).getY()
        if ownTask:
            taskMgr.add(self.update, "UpdateMouseLook")

    def disable(self):
        taskMgr.remove("UpdateMouseLook")

    def setPause(self, state):
        self.pause = state

    def clearMovement(self):
        self.camMove = dict(
            forward=False,
            backward=False,
            strafeLeft=False,
            strafeRight=False,
            down=False,
            up=False,
            )

    def setLimitH(self, left, right, relative=None):
        if relative is None:
            relative = render
        self.limitH = {
            "left": left,
            "right": right,
            "relative": relative
        }

    def enableMovement(self):
        self.accept("w", self.setCamMove, extraArgs=["forward", True])
        self.accept("w-up", self.setCamMove, extraArgs=["forward", False])
        self.accept("s", self.setCamMove, extraArgs=["backward", True])
        self.accept("s-up", self.setCamMove, extraArgs=["backward", False])
        self.accept("a", self.setCamMove, extraArgs=["strafeLeft", True])
        self.accept("a-up", self.setCamMove, extraArgs=["strafeLeft", False])
        self.accept("d", self.setCamMove, extraArgs=["strafeRight", True])
        self.accept("d-up", self.setCamMove, extraArgs=["strafeRight", False])

        self.accept("control", self.setCamMove, extraArgs=["down", True])
        self.accept("control-up", self.setCamMove, extraArgs=["down", False])
        self.accept("space", self.setCamMove, extraArgs=["up", True])
        self.accept("space-up", self.setCamMove, extraArgs=["up", False])

        self.accept("wheel_up", self.moveCamera, extraArgs=[Vec3(0, 1, 0)])
        self.accept("wheel_down", self.moveCamera, extraArgs=[Vec3(0, -1, 0)])

    def disableMovement(self):
        self.ignoreAll()

    def setCamMove(self, key, val):
        self.camMove[key] = val

    def centerMouse(self):
        winSizeX = self.targetWin.getXSize() / 2
        winSizeY = self.targetWin.getYSize() / 2

        self.targetWin.movePointer(0, winSizeX, winSizeY)

    def update(self, task=None):
        if self.pause:
            return PythonTask.cont

        if self.centerMouse:
            self.updateCenter()
        else:
            self.updateNoCenter()

        if self.limitH["left"] is not None:
            rel = self.limitH["relative"]
            h = self.targetCamera.getH(rel)

            if h < self.limitH["left"]:
                h = self.limitH["left"]
            elif h > self.limitH["right"]:
                h = self.limitH["right"]

            self.targetCamera.setH(rel, h)

        linVel = Vec3(0, 0, 0)
        if self.camMove["forward"]:
            linVel[1] = self.movementSpeed
        if self.camMove["backward"]:
            linVel[1] = -self.movementSpeed
        if self.camMove["strafeLeft"]:
            linVel[0] = -self.movementSpeed
        if self.camMove["strafeRight"]:
            linVel[0] = self.movementSpeed
        if self.camMove["up"]:
            linVel[2] = self.movementSpeed
        if self.camMove["down"]:
            linVel[2] = -self.movementSpeed

        linVel *= globalClock.getDt()
        self.moveCamera(linVel)

        return PythonTask.cont

    def updateCenter(self):
        winSizeX = self.targetWin.getXSize() / 2
        winSizeY = self.targetWin.getYSize() / 2

        mouse = self.targetWin.getPointer(0)

        deltaX = (mouse.getX() - winSizeX) * self.mouseLookSpeed[0]
        deltaY = (mouse.getY() - winSizeY) * self.mouseLookSpeed[1]

        if self.mouseLookMode == self.MLMFPP:
            self.updateFPP(deltaX, deltaY)
        elif self.mouseLookMode == self.MLMOrbit:
            self.updateOrbit(deltaX, deltaY)
        elif self.mouseLookMode == self.MLMPan:
            self.updatePan(deltaX, deltaY)

        self.updateAlternate(deltaX, deltaY)

        self.targetWin.movePointer(0, winSizeX, winSizeY)

    def updateNoCenter(self):
        mouse = self.targetWin.getPointer(0)
        x = mouse.getX()
        y = mouse.getY()

        deltaX = (x - self.prevX) * self.mouseLookSpeed[0]
        deltaY = (y - self.prevY) * self.mouseLookSpeed[1]

        self.prevX = x
        self.prevY = y

        self.updateAlternate(deltaX, deltaY)

    def updateAlternate(self, deltaX, deltaY):
        if self.mouseLookMode == self.MLMFPP:
            self.updateFPP(deltaX, deltaY)
        elif self.mouseLookMode == self.MLMOrbit:
            self.updateOrbit(deltaX, deltaY)
        elif self.mouseLookMode == self.MLMPan:
            self.updatePan(deltaX, deltaY)

    def moveCamera(self, vector):
        self.targetCamera.setPos(self.targetCamera, vector * self.wheelSpeed)

    def rotateAround(self, node, point, axis, angle, relative):
        quat = Quat()
        quat.setFromAxisAngle(angle, render.getRelativeVector(relative, axis))

        relativePos = node.getPos(render) - point
        relativePosRotated = quat.xform(relativePos)
        absolutePosRotated = relativePosRotated + point

        node.setPos(render, absolutePosRotated)
        node.setQuat(render, node.getQuat(render) * quat)

    def setTargetCamera(self, cam):
        if cam is None:
            self.targetCamera = base.camera
        else:
            self.targetCamera = cam

    def setTargetWin(self, win):
        if win is None:
            self.targetWin = base.win
        else:
            self.targetWin = win

    def setMouseModeRelative(self, state):
        props = WindowProperties()
        if not state:
            props.setMouseMode(WindowProperties.MAbsolute)
        else:
            props.setMouseMode(WindowProperties.MRelative)
        self.targetWin.requestProperties(props)

    def setCursorHidden(self, state):
        props = WindowProperties()
        props.setCursorHidden(state)
        self.targetWin.requestProperties(props)

    def updateFPP(self, deltaX, deltaY):
        #~ print "no center"
        p = self.targetCamera.getP(render) - deltaY
        h = self.targetCamera.getH(render) - deltaX
        if abs(p) > 90:
            p = 90 * cmp(p, 0)
        self.targetCamera.setP(p)
        self.targetCamera.setH(h)

    def updateOrbit(self, deltaX, deltaY):
        self.rotateAround(self.targetCamera, self.orbitCenter, Vec3(0, 0, 1), -deltaX, render)
        self.rotateAround(self.targetCamera, self.orbitCenter, Vec3(1, 0, 0), -deltaY, self.targetCamera)

    def updatePan(self, deltaX, deltaY):
        vector = Vec3(-deltaX, 0, deltaY) * 1 / globalClock.getDt() * 0.01
        self.moveCamera(vector)

if __name__ == "__main__":
    from direct.showbase.ShowBase import ShowBase
    import sys

    ShowBase()

    base.camLens.setFov(90.0)
    base.disableMouse()

    smiley = loader.loadModel("smiley")
    smiley.reparentTo(render)
    smiley.setScale(128)

    base.accept("escape", sys.exit)

    base.camera.setY(-1024)

    m = MouseLook()
    m.enable()
    m.enableMovement()
    m.setMouseModeRelative(True)
    m.setCursorHidden(True)

    mode = m.mouseLookMode

    def cycle():
        global mode
        mode += 1
        if mode > 3:
            mode = 0
        print mode
        m.mouseLookMode = mode

    base.accept("f1", cycle)

    run()
