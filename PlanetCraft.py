#PlanetCraft.py
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile
from panda3d.rocket import *
#uncomment and run when you add a block, then re comment on next run
#import BlockIniter
#import EntityIniter
#BlockIniter.initBlocks()
#EntityIniter.initBlocks()

from Blocks import *
from Entities import *
from Controls import *
import shelve
#import numpy as np

loadPrcFile("config/Config.prc")


class PlanetCraft(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.cont = Controls(self)
        self.cont.gameMode()
        self.setBackgroundColor(0, 0, 0, 1)
        gamma = Planet({'x': 0, 'y': 20, 'z': -2, 'render': self.render})

        #Pause menu overlay initialization
        self.ovrlay = False

        #I think we can (eventually) get away without this font
        LoadFontFace("tests/rocket-sample/assets/Delicious-Roman.otf")

        r = RocketRegion.make('pandaRocket', base.win)
        r.setActive(1)
        context = r.getContext()

        #we'll need to put the rml file in a final location evetually
        self.doc = context.LoadDocument('tests/rocketTest.rml')

        ih = RocketInputHandler()
        base.mouseWatcher.attachNewNode(ih)
        r.setInputHandler(ih)

    def stop(self):
        pass

    def overlay(self):
        self.ovrlay = not self.ovrlay

        if (self.ovrlay):
            self.doc.Show()
            self.cont.menuMode()
        else:
            self.doc.Hide()
            self.cont.gameMode()

app = PlanetCraft()
app.run()
