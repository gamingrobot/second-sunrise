#MAIN FILE
import sys
import os
import BlockManager
import EntityManager

import time
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
from ogre.renderer.OGRE.sf_OIS import *


class PlanetApplication(Application):

    def __init__(self):
        self.animationStates = []
        Application.__init__(self)
        if os.name == 'nt':
            self.plugins_path = "plugins.cfg.nt"
        else:
            self.plugins_path = "plugins.cfg.linux"
        self.resource_path = "resources.cfg"

    def _createScene(self):
        sceneManager = self.sceneManager
        sceneManager.setAmbientLight(ogre.ColourValue(1, 1, 1))
        sceneManager.setShadowTechnique(ogre.SHADOWTYPE_STENCIL_ADDITIVE)

        cube = sceneManager.createEntity('cube', 'cube.mesh')
        cube.setMaterialName ('Blocks/Stone')
        node = sceneManager.getRootSceneNode().createChildSceneNode("cube_node", ogre.Vector3(100, 50, 0))
        node.attachObject(cube)

        cube2 = sceneManager.createEntity('cube2', 'cube.mesh')
        cube2.setMaterialName ('Blocks/Grass')
        node2 = sceneManager.getRootSceneNode().createChildSceneNode("cube2_node", ogre.Vector3(0, 50, 0))
        node2.attachObject(cube2)


        # Create Camera
        self.camnode = sceneManager.getRootSceneNode().createChildSceneNode("CamNode1", ogre.Vector3(0, 25, 90))
        node = self.camnode.createChildSceneNode("PitchNode1")
        node.attachObject(self.camera)

    def _createCamera(self):
        self.camera = self.sceneManager.createCamera("PlayerCam")
        self.camera.nearClipDistance = 5

if __name__ == '__main__':
    print "Welcome to planet craft"
    #main()
    #sunexperiment()
    try:
        application = PlanetApplication()
        application.go()
    except ogre.OgreException, e:
        print e
