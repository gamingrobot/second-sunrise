from panda3d.core import Vec3, Point3, Quat, BitMask32
from panda3d.bullet import BulletCapsuleShape, BulletRigidBodyNode

import math


class Player:
    """A Player class - doesn't actually do that much, just arranges collision detection and provides a camera mount point, plus an interface for the controls to work with. All configured of course."""
    def __init__(self, xml):
        self.reload(xml)

    def reload(self, xml):
        """
        World -- (BulletWorld) the Bullet world.
        Parent -- (NodePath) where to parent the KCC elements
        walkHeight -- (float) height of the whole controller when walking
        crouchHeight -- (float) height of the whole controller when crouching
        stepHeight -- (float) maximum step height the caracter can walk.
        radius -- (float) capsule radius
        gravity -- (float) gravity setting for the character controller, currently as float (gravity is always down). The KCC may sometimes need a different gravity setting then the rest of the world. If this is not given, the gravity is same as world's
        """
        #walkHeight, crouchHeight, stepHeight, radius, gravity=None
        #2.0, 1.0, 0.0, 0.4
        #todo make in xml config
        walkHeight = 2.0
        crouchHeight = 1.0
        stepHeight = 0.0
        radius = 0.4
        gravity = 0.0

        self.__world = manager.get("physics").getWorld()
        self.__parent = render
        self.__timeStep = 0
        self.__currentPos = Vec3(0, 0, 0)

        self.movementParent = self.__parent.attachNewNode("Movement Parent")
        self.__setup(walkHeight, crouchHeight, stepHeight, radius)
        self.__mapMethods()

        #self.gravity = self.__world.getGravity() if gravity is None else gravity
        self.__world.setGravity(Vec3(0,0,gravity))
        self.gravity = self.__world.getGravity()
        self.setMaxSlope(90.0, True)
        self.setActiveJumpLimiter(True)

        self.movementState = "ground"
        self.movementStateFilter = {
            "ground": ["ground", "jumping", "falling"],
            "jumping": ["ground", "falling"],
            "falling": ["ground"],
            "flying": [],
        }

        # Prevent the KCC from moving when there's not enough room for it in the next frame
        # It doesn't work right now because I can't figure out how to add sliding. Sweep test could work, but it would cause problems with penetration testing and steps
        # That said, you probably won't need it, if you design your levels correctly
        self.predictFutureSpace = False
        self.futureSpacePredictionDistance = 10.0

        self.isCrouching = False

        self.__fallTime = 0.0
        self.__fallStartPosz = self.__currentPos.z
        self.__fallStartPosx = self.__currentPos.x
        self.__fallStartPosy = self.__currentPos.y
        self.__linearVelocity = Vec3(0, 0, 0)
        self.__headContact = None
        self.__footContact = None
        self.__enabledCrouch = False

        self.__standUpCallback = [None, [], {}]
        self.__fallCallback = [None, [], {}]

        manager.get("physics").registerPreFunc("playerController", self.update)

    def start(self):
        pass

    def stop(self):
        pass

    def destroy(self):
        pass

    """
    The custom kinematic character controller for Panda3D, replacing the Bullet's default character controller and providing more stability and features.

    Features included:
        * Walking with penetration prevention
        * Jumping with active and passive jump limiter. Active means limiting the max jump height based on the distance to the "ceiling". Passive means falling automatically when a "ceiling" is hit.
        * Crouching with stand up limiter which prevents the character from standing up if inside a tunnel or other limited space
        * Slope limiter of arbitrary maximum slope values which may or may not affect the movement speed on slopes smaller than maximum
        * Stepping, supports walking steps up and down (prevents "floating" effect)
        * Flying support for no-clip, ladders, swimming or simply flying
        * Simplified state system. Makes double/multiple jumps impossible by default
        * Callbacks for landing and standing up from crouch

    The controller is composed of a levitating capsule (allowing stepping), a kinematic body and numerous raycasts accounting for levitation and spacial awareness.
    The elements are set up automatically.
    """

    def setCollideMask(self, *args):
        self.__walkCapsuleNP.setCollideMask(*args)
        self.__crouchCapsuleNP.setCollideMask(*args)

    def setFallCallback(self, method, args=[], kwargs={}):
        """
        Callback called when the character falls on thge ground.

        The position where falling started is passed as the first argument, the additional argument and keyword arguments follow.
        """
        self.__fallCallback = [method, args, kwargs]

    def setStandUpCallback(self, method, args=[], kwargs={}):
        """
        Callback called when the character stands up from crouch. This is needed because standing up might be prevented by spacial awareness.
        """
        self.__standUpCallback = [method, args, kwargs]

    def setMaxSlope(self, degs, affectSpeed):
        """
        degs -- (float) maximum slope in degrees. 0, False or None means don't limit slope.
        affectSpeed -- (bool) if True, the character will walk slower up slopes

        Both options are independent.

        By default, affectSpeed is enabled and maximum slope is 50 deg.
        """
        if not degs:
            self.minSlopeDot = None
            return
        self.minSlopeDot = round(math.cos(math.radians(degs)), 2)

        self.__slopeAffectsSpeed = affectSpeed

    def setActiveJumpLimiter(self, val):
        """
        Enable or disable the active jump limiter, which is the mechanism that changes the maksimum jump height based on the space available above the character's head.
        """
        self.__intelligentJump = val

    def startCrouch(self):
        self.isCrouching = True
        self.__enabledCrouch = True

        self.__capsule = self.__crouchCapsule
        self.__capsuleNP = self.__crouchCapsuleNP

        self.__capsuleH, self.__levitation, self.__capsuleR, self.__h = self.__crouchCapsuleH, self.__crouchLevitation, self.__crouchCapsuleR, self.__crouchH

        self.__world.removeRigidBody(self.__walkCapsuleNP.node())
        self.__world.attachRigidBody(self.__crouchCapsuleNP.node())

        #self.__capsuleOffset = self.__capsuleH * 0.5 + self.__levitation
        self.__capsuleOffset = self.__capsuleH
        self.__footDistance = self.__capsuleOffset + self.__levitation

    def stopCrouch(self):
        """
        Note that spacial awareness may prevent the character from standing up immediately, which is what you usually want. Use stand up callback to know when the character stands up.
        """
        self.__enabledCrouch = False

    def isOnGround(self):
        """
        Check if the character is on ground. You may also check if the movementState variable is set to 'ground'
        """
        if self.__footContact is None:
            return False
        elif self.movementState == "ground":
            elevation = self.__currentPos.z - self.__footContact[0].z
            return (elevation <= self.__levitation + 0.02)
        else:
            return self.__currentPos <= self.__footContact[0]

    def startJump(self, maxHeight=3.0):
        """
        max height is 3.0 by default. Probably too much for most uses.
        """
        self.__jump(maxHeight)

    def startFly(self):
        self.movementState = 'flying'

    def stopFly(self):
        """
        Stop flying and start falling
        """
        self.__fall()

    def setAngularMovement(self, omega):
        self.movementParent.setH(self.movementParent, omega * self.__timeStep)

    def setLinearMovement(self, speed, *args):
        self.__linearVelocity = speed

    def update(self):
        """
        Update method. Call this around doPhysics.
        """
        #self.gravity = self.__world.getGravity()
        processStates = {
            "ground": self.__processGround,
            "jumping": self.__processJumping,
            "falling": self.__processFalling,
            "flying": self.__processFlying,
        }

        self.__timeStep = globalClock.getDt()

        self.__updateFootContact()
        self.__updateHeadContact()

        processStates[self.movementState]()

        self.__applyLinearVelocity()
        self.__preventPenetration()

        self.__updateCapsule()

        if self.isCrouching and not self.__enabledCrouch:
            self.__standUp()

    def __land(self):
        self.movementState = "ground"
        log.info("new state", self.movementState)

    def __fall(self):
        self.movementState = "falling"

        self.__fallStartPosz = self.__currentPos.z
        self.__fallStartPosx = self.__currentPos.x
        self.__fallStartPosy = self.__currentPos.y
        self.fallDelta = 0.0
        self.__fallTime = 0.0

        log.info("new state", self.movementState)

    def __jump(self, maxZ=3.0):
        if "jumping" not in self.movementStateFilter[self.movementState]:
            return

        maxZ += self.__currentPos.z

        if self.__intelligentJump and self.__headContact is not None and self.__headContact[0].z < maxZ + self.__h:
            maxZ = self.__headContact[0].z - self.__h * 1.2

        maxZ = round(maxZ, 2)

        self.jumpStartPos = self.__currentPos.z
        self.jumpTime = 0.0

        bsq = -4.0 * self.gravity.z * (maxZ - self.jumpStartPos)
        try:
            b = math.sqrt(bsq)
        except:
            return
        self.jumpSpeed = b
        self.jumpMaxHeight = maxZ

        self.movementState = "jumping"

    def __standUp(self):
        self.__updateHeadContact()

        if self.__headContact is not None and self.__currentPos.z + self.__walkLevitation + self.__walkCapsuleH >= self.__headContact[0].z:
            return

        self.isCrouching = False

        self.__capsule = self.__walkCapsule
        self.__capsuleNP = self.__walkCapsuleNP

        self.__capsuleH, self.__levitation, self.__capsuleR, self.__h = self.__walkCapsuleH, self.__walkLevitation, self.__walkCapsuleR, self.__walkH

        self.__world.removeRigidBody(self.__crouchCapsuleNP.node())
        self.__world.attachRigidBody(self.__walkCapsuleNP.node())

        #self.__capsuleOffset = self.__capsuleH * 0.5 + self.__levitation
        self.__capsuleOffset = self.__capsuleH
        self.__footDistance = self.__capsuleOffset + self.__levitation

        if self.__standUpCallback[0] is not None:
            self.__standUpCallback(*self.__standUpCallback[1], **self.__standUpCallback[2])

    def __processGround(self):
        if not self.isOnGround():
            self.__fall()
        else:
            self.__currentPos.z = self.__footContact[0].z

    def __processFalling(self):
        self.__fallTime += self.__timeStep
        self.fallDeltaz = self.gravity.z * (self.__fallTime) ** 2
        #self.fallDeltax = self.gravity.x * (self.__fallTime) ** 2
        #self.fallDeltay = self.gravity.y * (self.__fallTime) ** 2

        newPos = Vec3(self.__currentPos)
        newPos.z = self.__fallStartPosz + self.fallDeltaz
        #newPos.x = self.__fallStartPosx + self.fallDeltax
        #newPos.y = self.__fallStartPosy + self.fallDeltay

        self.__currentPos = newPos

        if self.isOnGround():
            self.__land()
            if self.__fallCallback[0] is not None:
                self.__fallCallback(self.__fallStartPos, *self.__fallCallback[1], **self.__fallCallback[2])

    def __processJumping(self):
        if self.__headContact is not None and self.__capsuleTop >= self.__headContact[0].z:
            # This shouldn't happen, but just in case, if we hit the ceiling, we start to fall
            log.info("Head bang")
            self.__fall()
            return

        oldPos = float(self.__currentPos.z)

        self.jumpTime += self.__timeStep
        #set horazontal gravity here
        self.__currentPos.z = (self.gravity.z * self.jumpTime ** 2) + (self.jumpSpeed * self.jumpTime) + self.jumpStartPos

        if round(self.__currentPos.z, 2) >= self.jumpMaxHeight:
            self.__fall()

    def __processFlying(self):
        if self.__footContact and self.__currentPos.z - 0.1 < self.__footContact[0].z and self.__linearVelocity.z < 0.0:
            self.__currentPos.z = self.__footContact[0].z
            self.__linearVelocity.z = 0.0

        if self.__headContact and self.__capsuleTop >= self.__headContact[0].z and self.__linearVelocity.z > 0.0:
            self.__linearVelocity.z = 0.0

    def __checkFutureSpace(self, globalVel):
        globalVel = globalVel * self.futureSpacePredictionDistance

        pFrom = Point3(self.__capsuleNP.getPos(render) + globalVel)
        pUp = Point3(pFrom + Point3(0, 0, self.__capsuleH * 2.0))
        pDown = Point3(pFrom - Point3(0, 0, self.__capsuleH * 2.0 + self.__levitation))

        upTest = self.__world.rayTestClosest(pFrom, pUp)
        downTest = self.__world.rayTestClosest(pFrom, pDown)

        if not (upTest.hasHit() and downTest.hasHit):
            return True

        upNode = upTest.getNode()
        if upNode.getMass():
            return True

        space = abs(upTest.getHitPos().z - downTest.getHitPos().z)

        if space < self.__levitation + self.__capsuleH + self.__capsule.getRadius():
            return False

        return True

    def __updateFootContact(self):
        pFrom = Point3(self.__capsuleNP.getPos(render))
        pTo = Point3(pFrom - Point3(0, 0, self.__footDistance))
        rayTest = self.__world.rayTestClosest(pFrom, pTo)

        if not rayTest.hasHit():
            self.__footContact = None
            return

        self.__footContact = [rayTest.getHitPos(), rayTest.getNode(), rayTest.getHitNormal()]

    def __updateHeadContact(self):
        pFrom = Point3(self.__capsuleNP.getPos(render))
        pTo = Point3(pFrom + Point3(0, 0, self.__capsuleH * 20.0))
        rayTest = self.__world.rayTestClosest(pFrom, pTo)

        if rayTest.hasHit():
            self.__headContact = [rayTest.getHitPos(), rayTest.getNode()]
        else:
            self.__headContact = None

    def __updateCapsule(self):
        self.movementParent.setPos(self.__currentPos)
        self.__capsuleNP.setPos(0, 0, self.__capsuleOffset)

        self.__capsuleTop = self.__currentPos.z + self.__levitation + self.__capsuleH * 2.0

    def __applyLinearVelocity(self):
        globalVel = self.movementParent.getQuat(render).xform(self.__linearVelocity) * self.__timeStep

        if self.predictFutureSpace and not self.__checkFutureSpace(globalVel):
            return

        if self.__footContact is not None and self.minSlopeDot and self.movementState != "flying":
            normalVel = Vec3(globalVel)
            normalVel.normalize()

            floorNormal = self.__footContact[2]
            absSlopeDot = round(floorNormal.dot(Vec3.up()), 2)

            def applyGravity():
                self.__currentPos -= Vec3(floorNormal.x, floorNormal.y, floorNormal.z) * self.gravity * self.__timeStep * 0.1

            if absSlopeDot <= self.minSlopeDot:
                applyGravity()

                if globalVel != Vec3():
                    globalVelDir = Vec3(globalVel)
                    globalVelDir.normalize()

                    fn = Vec3(floorNormal.x, floorNormal.y, 0.0)
                    fn.normalize()

                    velDot = 1.0 - globalVelDir.angleDeg(fn) / 180.0
                    if velDot < 0.5:
                        self.__currentPos -= Vec3(fn.x * globalVel.x, fn.y * globalVel.y, globalVel.z) * velDot

                    globalVel *= velDot

            elif self.__slopeAffectsSpeed and globalVel != Vec3():
                applyGravity()

        self.__currentPos += globalVel

    def __preventPenetration(self):
        collisions = Vec3()
        ##########################################################
        # This is a hacky version for when contactTest didn't work
        #~ for mf in self.__world.getManifolds():
            #~ if not (mf.getNumManifoldPoints() and self.__capsuleNP.node() in [mf.getNode0(), mf.getNode1()]):
                #~ continue
            #~
            #~ sign = 1 if mf.getNode0() == self.__capsuleNP.node() else -1
            #~
            #~ for mpoint in mf.getManifoldPoints():
                #~ direction = mpoint.getPositionWorldOnB() - mpoint.getPositionWorldOnA()
                #~ normal = Vec3(direction)
                #~ normal.normalize()
                #~
                #~ if mpoint.getDistance() < 0:
                    #~ collisions -= direction * mpoint.getDistance() * 2.0 * sign

        result = self.__world.contactTest(self.__capsuleNP.node())

        for i, contact in enumerate(result.getContacts()):
            mpoint = contact.getManifoldPoint()
            normal = mpoint.getPositionWorldOnB() - mpoint.getPositionWorldOnA()

            if mpoint.getDistance() < 0:
                collisions -= normal * mpoint.getDistance()

        collisions.z = 0.0
        self.__currentPos += collisions

    def __mapMethods(self):
        self.getHpr = self.movementParent.getHpr
        self.getH = self.movementParent.getH
        self.getP = self.movementParent.getP
        self.getR = self.movementParent.getR

        self.getPos = self.movementParent.getPos
        self.getX = self.movementParent.getX
        self.getY = self.movementParent.getY
        self.getZ = self.movementParent.getZ

        self.getQuat = self.movementParent.getQuat

        self.setHpr = self.movementParent.setHpr
        self.setH = self.movementParent.setH
        self.setP = self.movementParent.setP
        self.setR = self.movementParent.setR

        #self.setPos = self.movementParent.setPos
        self.setX = self.movementParent.setX
        self.setY = self.movementParent.setY
        self.setZ = self.movementParent.setZ

        self.headsUp = self.movementParent.headsUp

        self.setQuat = self.movementParent.setQuat

    def setPos(self, vector):
        self.movementParent.setPos(vector)
        self.__currentPos = vector


    def __setup(self, walkH, crouchH, stepH, R):
        def setData(fullH, stepH, R):
            if fullH - stepH <= R * 2.0:
                length = 0.1
                R = (fullH * 0.5) - (stepH * 0.5)
                lev = stepH + R
            else:
                length = fullH - stepH - R * 2.0
                lev = fullH - R - length / 2.0

            return length, lev, R

        self.__walkH = walkH
        self.__crouchH = crouchH

        self.__walkCapsuleH, self.__walkLevitation, self.__walkCapsuleR = setData(walkH, stepH, R)
        self.__crouchCapsuleH, self.__crouchLevitation, self.__crouchCapsuleR = setData(crouchH, stepH, R)

        self.__capsuleH, self.__levitation, self.__capsuleR, self.__h = self.__walkCapsuleH, self.__walkLevitation, self.__walkCapsuleR, self.__walkH

        #self.__capsuleOffset = self.__capsuleH * 0.5 + self.__levitation
        self.__capsuleOffset = self.__capsuleH
        self.__footDistance = self.__capsuleOffset + self.__levitation

        self.__addElements()

    def __addElements(self):
        # Walk Capsule
        self.__walkCapsule = BulletCapsuleShape(self.__walkCapsuleR, self.__walkCapsuleH)

        self.__walkCapsuleNP = self.movementParent.attachNewNode(BulletRigidBodyNode('Capsule'))
        self.__walkCapsuleNP.node().addShape(self.__walkCapsule)
        self.__walkCapsuleNP.node().setKinematic(True)
        self.__walkCapsuleNP.setCollideMask(BitMask32.allOn())

        self.__world.attachRigidBody(self.__walkCapsuleNP.node())

        # Crouch Capsule
        self.__crouchCapsule = BulletCapsuleShape(self.__crouchCapsuleR, self.__crouchCapsuleH)

        self.__crouchCapsuleNP = self.movementParent.attachNewNode(BulletRigidBodyNode('crouchCapsule'))
        self.__crouchCapsuleNP.node().addShape(self.__crouchCapsule)
        self.__crouchCapsuleNP.node().setKinematic(True)
        self.__crouchCapsuleNP.setCollideMask(BitMask32.allOn())

        # Set default
        self.__capsule = self.__walkCapsule
        self.__capsuleNP = self.__walkCapsuleNP

        # Init
        self.__updateCapsule()