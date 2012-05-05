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
#import numpy as np

loadPrcFile("config/Config.prc")


class PlanetCraft(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        Controls(self)
        self.setBackgroundColor(0, 0, 0, 1)
        Planet({'x': 0, 'y': 20, 'z': -2, 'render': self.render})

        print Core
        print Space
        print Player
        p = Player("oh hai")
        a = Air({'x': 4, 'y': 2, 'z': 7})
        print a
        print p

app = PlanetCraft()
app.run()
