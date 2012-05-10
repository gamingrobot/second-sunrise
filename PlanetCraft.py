#PlanetCraft.py
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile
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
        gamma = Planet({'x': 0, 'y': 20, 'z': -2, 'render': self.render})


    def stop(self):
        pass


app = PlanetCraft()
app.run()
