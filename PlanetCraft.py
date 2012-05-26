#PlanetCraft.py
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile
from panda3d.core import PointLight
from panda3d.core import AmbientLight
from panda3d.core import VBase4
from panda3d.core import Point3
#uncomment and run when you add a block, then re comment on next run
#import BlockIniter
#import EntityIniter
#BlockIniter.initBlocks()
#EntityIniter.initBlocks()

from Blocks import *
from Entities import *
from Controls import *
#import shelve
#import numpy as np

loadPrcFile("config/Config.prc")


class PlanetCraft(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.cont = Controls(self)
        self.cont.gameMode()
        self.setBackgroundColor(0, 0, 0, 1)
        print self.camera.getPos()
        gamma = Planet({'x': -48, 'y': 16, 'z': -48, 'render': self.render})

        """plight = PointLight('plight')
        plight.setColor(VBase4(1, 1, 1, 1))
        #plight.setAttenuation(Point3(0, 0, 0.5))
        plnp = self.render.attachNewNode(plight)
        plnp.setPos(0, 0, 0)
        self.render.setLight(plnp)"""

        """alight = AmbientLight('alight')
        alight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)"""

        centx, centy, centz = gamma.getCenter()
        print str(centx) + str(centy) + str(centz)

    def stop(self):
        pass


app = PlanetCraft()
app.run()
