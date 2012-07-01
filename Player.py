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
        #create hud
        self.hud = Hud(self.root)
        #create ingamemenu
        self.ingamemenu = InGameMenu(self.root, self)
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

        #setup picking
        #add mouse button 1 handler
        self.root.accept('mouse1', self.onMouseTask)
        #add mouse collision to our world
        self.setupMouseCollision()

    def doExit(self):
        self.cleanup()
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

        self.character.setH(base.camera.getH(render))
        self.character.update()  # WIP

        #self.ml.orbitCenter = self.character.getPos(render)
        #base.camera.setPos(base.camera.getPos(render) + delta)"""
        base.camera.setPos(self.character.getPos(render) + Vec3(0, 0, 2))

    def cleanup(self):
        self.world = None
        self.worldNP.removeNode()

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

    def onMouseTask(self):
        """ """
        #do we have a mouse
        if (self.root.mouseWatcherNode.hasMouse() == False):
            return

        #get the mouse position
        mpos = base.mouseWatcherNode.getMouse()

        #Set the position of the ray based on the mouse position
        self.mPickRay.setFromLens(self.root.camNode, mpos.getX(), mpos.getY())

        #for this small example I will traverse everything, for bigger projects
        #this is probably a bad idea
        self.mPickerTraverser.traverse(self.root.render)

        if (self.mCollisionQue.getNumEntries() > 0):
            self.mCollisionQue.sortEntries()
            entry = self.mCollisionQue.getEntry(0)
            chunk = entry.getIntoNodePath()

            chunk = chunk.findNetTag('Pickable')
            if not chunk.isEmpty():
                #here is how you get the surface collsion
                block = entry.getSurfacePoint(self.root.render)
                chunkname = chunk.getName()
                cord = chunkname.split(":")

                x = int(math.floor(block[0] - int(cord[0])))
                y = int(math.floor(block[1] - int(cord[1])))
                z = int(math.floor(block[2] - int(cord[2])))
                print block
                print chunkname
                print str(x) + "," + str(y) + "," + str(z)

                self.planet.removeBlock(chunkname, x, y, z)
                #handleBlockClick(chunk, block)

    def setupMouseCollision(self):
        """ """
        #Since we are using collision detection to do picking, we set it up
        #any other collision detection system with a traverser and a handler
        self.mPickerTraverser = CollisionTraverser()  # Make a traverser
        self.mCollisionQue = CollisionHandlerQueue()

        #create a collision solid ray to detect against
        self.mPickRay = CollisionRay()
        self.mPickRay.setOrigin(self.root.camera.getPos(self.root.render))
        self.mPickRay.setDirection(render.getRelativeVector(camera, Vec3(0, 1, 0)))

        #create our collison Node to hold the ray
        self.mPickNode = CollisionNode('pickRay')
        self.mPickNode.addSolid(self.mPickRay)

        #Attach that node to the camera since the ray will need to be positioned
        #relative to it, returns a new nodepath
        #well use the default geometry mask
        #this is inefficent but its for mouse picking only

        self.mPickNP = self.root.camera.attachNewNode(self.mPickNode)

        #well use what panda calls the "from" node.  This is reall a silly convention
        #but from nodes are nodes that are active, while into nodes are usually passive environments
        #this isnt a hard rule, but following it usually reduces processing

        #Everything to be picked will use bit 1. This way if we were doing other
        #collision we could seperate it, we use bitmasks to determine what we check other objects against
        #if they dont have a bitmask for bit 1 well skip them!
        self.mPickNode.setFromCollideMask(GeomNode.getDefaultCollideMask())

        #Register the ray as something that can cause collisions
        self.mPickerTraverser.addCollider(self.mPickNP, self.mCollisionQue)
        #if you want to show collisions for debugging turn this on
        #self.mPickerTraverser.showCollisions(self.render)

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
