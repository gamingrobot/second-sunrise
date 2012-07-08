#Player
import sys
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import BulletBoxShape
from panda3d.core import Vec3
from panda3d.core import PointLight
from panda3d.core import Vec4
from panda3d.core import WindowProperties
from panda3d.core import VBase4
from panda3d.core import CollisionRay, CollisionNode, GeomNode, CollisionTraverser
from panda3d.core import CollisionHandlerQueue, CollisionSphere, BitMask32
from panda3d.core import GeomVertexFormat
from panda3d.core import GeomVertexData
from panda3d.core import GeomVertexWriter
from panda3d.core import GeomLines
from panda3d.core import GeomNode
from panda3d.core import Geom
import math
from CharacterController import *
from mouseLook import MouseLook
from direct.showbase.InputStateGlobal import inputState
from Controls import *
from Hud import *
from Menus import InGameMenu


class Player:
    """Player"""
    def __init__(self, args):
        self.root = args['root']
        self.planet = args['planet']
        #setup camera
        self.root.camera.setPos(args['x'], args['y'], args['z'])
        plight = PointLight('plight')
        plight.setColor(VBase4(1, 1, 1, 1))
        #plight.setAttenuation(Point3(0, 0, 0.5))
        plnp = self.root.camera.attachNewNode(plight)
        plnp.setPos(0, 0, 0)
        self.root.render.setLight(plnp)
        self.selection = None
        #create hud
        self.hud = Hud(self.root)
        #create ingamemenu
        self.ingamemenu = InGameMenu(self.root, self)
        self.currentchunk = None
        #setup controls
        base.disableMouse()

        self.ml = MouseLook()
        self.ml.setMouseModeRelative(True)
        self.ml.setCursorHidden(True)
        self.ml.centerMouse = True
        self.ml.mouseLookMode = self.ml.MLMFPP
        self.ml.wheelSpeed = 1.0
        self.ml.enable()

        #~ base.accept("mouse2", ml.enable)
        #~ base.accept("mouse2-up", ml.disable)
        base.accept("wheel_up", self.ml.moveCamera, extraArgs=[Vec3(0, 1, 0)])
        base.accept("wheel_down", self.ml.moveCamera, extraArgs=[Vec3(0, -1, 0)])

        base.cam.node().getLens().setFov(70.0)

        """self.mouseChangeX = 0
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

        #hide mouse
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)
        #set game bool
        self.startLook()"""

        #globalClock.setMode(globalClock.MLimited)
        #globalClock.setFrameRate(120.0)

        # Input
        self.root.accept('escape', self.doExit)
        self.root.accept('space', self.doJump)
        self.root.accept('mouse1', self.removeBlock)
        self.root.accept('mouse3', self.placeBlock)
        #self.accept('c', self.doCrouch)
        #self.accept('c-up', self.stopCrouch)

        self.root.accept('control', self.startFly)
        self.root.accept('control-up', self.stopFly)

        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('left', 'a')
        inputState.watchWithModifiers('reverse', 's')
        inputState.watchWithModifiers('right', 'd')
        inputState.watchWithModifiers('turnLeft', 'q')
        inputState.watchWithModifiers('turnRight', 'e')

        inputState.watchWithModifiers('run', 'shift')

        inputState.watchWithModifiers('flyUp', 'r')
        inputState.watchWithModifiers('flyDown', 'f')

        # Physics
        #self.playernp = self.root.render.attachNewNode('Player')
        self.character = CharacterController(self.root.bulletworld, self.root.render, 2.0, 1.0, 0.0, 0.4)
        #self.character.setPos(render, Point3(0, 0, 0.5))

        #self.root.camera.reparentTo(self.character.movementParent)
        #self.root.camera.setPos(0, 0, 0.5)

        """#create player mesh
        shape = BulletBoxShape(Vec3(0.5, 0.5, 1))
        #self.bplayer = BulletRigidBodyNode('Player')
        self.bplayer = BulletCharacterControllerNode(shape, 1.0, 'Player')
        self.bplayer.setMaxSlope(1.5)
        #self.bplayer.setMass(200)
        #self.bplayer.addShape(shape)
        #self.bplayer.setDeactivationEnabled(False)
        self.player = self.root.render.attachNewNode(self.bplayer)
        self.player.setPos(args['x'], args['y'], args['z'])
        self.root.bulletworld.attachCharacter(self.bplayer)
        #model = self.root.loader.loadModel('models/box.egg')
        #model.flattenLight()
        #model.reparentTo(self.player)
        #model.setPos(-0.5, -0.5, -0.5)
        #reparent player to camera
        self.root.camera.reparentTo(self.player)
        #start the controller
        self.cont = Controls(self.root, self)

        self.root.camera.setPos(0, 0, 0.5)

        #was used before start menu was working
        #self.cont.gameMode()"""

        #create selection mesh
        format = GeomVertexFormat.registerFormat(GeomVertexFormat.getV3n3c4t2())
        vdata = GeomVertexData('chunk', format, Geom.UHStatic)

        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color = GeomVertexWriter(vdata, 'color')
        texcoord = GeomVertexWriter(vdata, 'texcoord')

        prim = GeomLines(Geom.UHStatic)
        shade = 1.0

        #0
        vertex.addData3f(0, 0, 0)
        normal.addData3f(0, 0, 1)
        color.addData4f(shade, 0.0, 0.0, 1)
        texcoord.addData2f(0, 0)

        #1
        vertex.addData3f(0, 1, 0)
        normal.addData3f(0, 0, 1)
        color.addData4f(shade, 0.0, 0.0, 1)
        texcoord.addData2f(0, 0)

        #2
        vertex.addData3f(1, 1, 0)
        normal.addData3f(0, 0, 1)
        color.addData4f(shade, 0.0, 0.0, 1)
        texcoord.addData2f(0, 0)

        #3
        vertex.addData3f(1, 0, 0)
        normal.addData3f(0, 0, 1)
        color.addData4f(shade, 0.0, 0.0, 1)
        texcoord.addData2f(0, 0)

        #top side
        prim.addVertices(0, 1)
        prim.addVertices(1, 2)
        prim.addVertices(2, 3)
        prim.addVertices(3, 0)

        #4
        vertex.addData3f(0, 0, -1)
        normal.addData3f(0, 0, 1)
        color.addData4f(shade, 0.0, 0.0, 1)
        texcoord.addData2f(0, 0)

        #5
        vertex.addData3f(0, 1, -1)
        normal.addData3f(0, 0, 1)
        color.addData4f(shade, 0.0, 0.0, 1)
        texcoord.addData2f(0, 0)

        #6
        vertex.addData3f(1, 1, -1)
        normal.addData3f(0, 0, 1)
        color.addData4f(shade, 0.0, 0.0, 1)
        texcoord.addData2f(0, 0)

        #7
        vertex.addData3f(1, 0, -1)
        normal.addData3f(0, 0, 1)
        color.addData4f(shade, 0.0, 0.0, 1)
        texcoord.addData2f(0, 0)

        #bottom side
        prim.addVertices(4, 5)
        prim.addVertices(5, 6)
        prim.addVertices(6, 7)
        prim.addVertices(7, 4)

        #other sides
        prim.addVertices(0, 4)
        prim.addVertices(1, 5)
        prim.addVertices(2, 6)
        prim.addVertices(3, 7)

        prim.closePrimitive()
        #attach primitives and render
        geom = Geom(vdata)
        geom.addPrimitive(prim)

        #add bullet
        """col = BulletTriangleMesh()
        col.addGeom(geom)
        shape = BulletTriangleMeshShape(col, dynamic=False)
        bulletnode = BulletRigidBodyNode('Chunk')
        bulletnode.addShape(shape)
        bulletnp = self.planetNode.attachNewNode(bulletnode)
        bulletnp.setPos(self.x + self.size, self.y + self.size, self.z + self.size)
        self.root.bulletworld.attachRigidBody(bulletnode)"""

        node = GeomNode('picker')
        node.addGeom(geom)
        self.select = self.root.render.attachNewNode(node)
        self.select.setPos(0, 0, 0)

        """self.select = self.root.loader.loadModel('models/box.egg')
        self.select.reparentTo(self.root.render)
        self.select.setPos(0, 0, 0)"""

    def doExit(self):
        #self.cleanup()
        sys.exit(1)

    def doJump(self):
        self.character.startJump(10)

    def doCrouch(self):
        self.character.startCrouch()

    def stopCrouch(self):
        self.character.stopCrouch()

    def startFly(self):
        self.character.startFly()

    def stopFly(self):
        self.character.stopFly()

    def processInput(self, dt):
        speed = Vec3(0, 0, 0)
        omega = 0.0

        v = 5.0

        if inputState.isSet('run'): v = 15.0

        if inputState.isSet('forward'): speed.setY(v)
        if inputState.isSet('reverse'): speed.setY(-v)
        if inputState.isSet('left'):    speed.setX(-v)
        if inputState.isSet('right'):   speed.setX(v)

        if inputState.isSet('flyUp'):   speed.setZ( 2.0)
        if inputState.isSet('flyDown'):   speed.setZ( -2.0)

        if inputState.isSet('turnLeft'):  omega =  120.0
        if inputState.isSet('turnRight'): omega = -120.0

        self.character.setAngularMovement(omega)
        self.character.setLinearMovement(speed, True)

    def update(self):
        dt = globalClock.getDt()

        self.processInput(dt)

        self.character.setH(base.camera.getH())
        self.character.update()  # WIP

        #self.ml.orbitCenter = self.character.getPos(render)
        #base.camera.setPos(base.camera.getPos(render) + delta)"""
        base.camera.setPos(self.character.getPos() + Vec3(0, 0, 2))

        #find what chunk the player is in
        charpos = self.character.getPos()
        charx = int(math.floor(charpos.getX()))
        chary = int(math.floor(charpos.getY()))
        charz = int(math.floor(charpos.getZ()))
        currentcord = self.currentchunk.split(":")
        newx = currentcord[0]
        newy = currentcord[1]
        newz = currentcord[2]
        #check naboring chunks to see if player is close to them
        for key, value in self.planet.chunks.items():
            cords = key.split(":")
            cordx = int(cords[0])
            cordy = int(cords[1])
            cordz = int(cords[2])
            #check x
            if charx >= cordx and charx < cordx + 16:
                newx = cordx

            #check y
            if chary >= cordy and chary < cordy + 16:
                newy = cordy

            #check z
            if charz >= cordz and charz < cordz + 16:
                newz = cordz

        chunk = self.planet.genHash(newx, newy, newz)
        if self.planet.playerchunk != chunk:
            self.currentchunk = chunk
            self.planet.playerchunk = self.currentchunk
            #print self.planet.playerchunk
            self.planet.playerChangedChunk()

        #do picking
        # Get to and from pos in camera coordinates
        pMouse = base.mouseWatcherNode.getMouse()
        pFrom = Point3()
        pTo = Point3()
        base.camLens.extrude(pMouse, pFrom, pTo)

        # Transform to global coordinates
        pFrom = render.getRelativePoint(base.cam, pFrom)
        pTo = render.getRelativePoint(base.cam, pTo)

        result = self.root.bulletworld.rayTestClosest(pFrom, pTo)
        """if result.hasHit():
            print result.getHitPos()
            print result.getHitNormal()
            print result.getHitFraction()
            print result.getNode().getName()"""
        if result.hasHit():
            #here is how you get the surface collsion
            block = result.getHitPos()
            chunkname = result.getNode().getName()
            cord = chunkname.split(":")

            x = int(round(block[0] - int(cord[0]), 0) - 1)
            y = int(round(block[1] - int(cord[1]), 0) - 1)
            z = int(round(block[2] - int(cord[2]), 0) - 1)
            #print block
            #print chunkname
            #print str(x) + "," + str(y) + "," + str(z)

            #self.planet.removeBlock(chunkname, x, y, z)
            self.selection = (chunkname, (x, y, z))
            self.select.setPos(int(math.floor(block[0])), int(math.floor(block[1])), int(math.floor(block[2])))
            #print (int(math.floor(block[0])), int(math.floor(block[1])), int(math.floor(block[2])))
        else:
            self.selection = None

    #def cleanup(self):
     #   self.world = None
        #self.worldNP.removeNode()

    def removeBlock(self):
        print "Removing Block"
        if self.selection != None:
            self.planet.removeBlock(self.selection[0], self.selection[1][0], self.selection[1][1], self.selection[1][2])

    def placeBlock(self):
        print "Placing Block"
        if self.selection != None:
            self.planet.placeBlock(self.selection[0], self.selection[1][0], self.selection[1][1], self.selection[1][2] + 1)

    def look(self, task):
        mouse = self.root.win.getPointer(0)
        x = mouse.getX()
        y = mouse.getY()
        if self.root.win.movePointer(0, self.centerX, self.centerY):
            self.mouseChangeX = self.centerX - x
            self.mouseChangeY = self.centerY - y
            self.H += self.mouseChangeX * self.sensitivity
            self.P += self.mouseChangeY * self.sensitivity
            self.root.camera.setP(self.P)
            self.root.camera.setH(self.H)
            #print "H" + str(self.H)
            #print "P" + str(self.P)
        return Task.cont

    def startLook(self):
        self.root.win.movePointer(0, self.centerX, self.centerY)
        taskMgr.add(self.look, 'look')

    def getPos(self):
        return self.character.getPos()

    def setPos(self, newpos):
        self.character.setPos(newpos)

    def getMass(self):
        return self.bplayer.getMass()

    def applyForce(self, force, mode):
        self.bplayer.applyForce(force, mode)

    def setLinearVelocity(self, force):
        self.bplayer.setLinearVelocity(force)

    def setAngularVelocity(self, omega):
        self.bplayer.setAngularVelocity(omega)

    def setLinearMovement(self, force):
        self.bplayer.setLinearMovement(force, True)

    def setAngularMovement(self, omega):
        self.bplayer.setAngularMovement(omega)

    def getLinearVelocity(self):
        return self.bplayer.getLinearVelocity()

    def getAngularVelocity(self):
        return self.bplayer.getAngularVelocity()

    def headsUp(self, planet):
        self.character.headsUp(planet)

    def setHpr(self, h, p, r):
        self.player.setHpr(h, p, r)

    def toggleInGameMenu(self):
        if self.cont.inGame:
            self.ingamemenu.doc.Show()
            self.cont.menuMode()
        else:
            self.ingamemenu.doc.Hide()
            self.cont.gameMode()

    def stop(self):
        self.cont.stop()
