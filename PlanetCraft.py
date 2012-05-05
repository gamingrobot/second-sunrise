#PlanetCraft.py
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile
import BlockManager
#BlockManager.initBlocks()
from Blocks import *
#from Blocks.Air import *
from Controls import *
#import numpy as np

loadPrcFile("config/Config.prc")


class PlanetCraft(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        Controls(self, True)
        print Core
        print Space
        a = Air({'x': 4, 'y': 2, 'z': 7})
        print a

app = PlanetCraft()
app.run()
