#PlanetCraft.py
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile
from Controls import *
import EntityManager
#import numpy as np

loadPrcFile("config/Config.prc")


class PlanetCraft(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        Controls(self)
        self.setBackgroundColor(0, 0, 0, 1)
        EntityManager.Planet({'x': 0, 'y': 20, 'z': -2, 'render': self.render})

app = PlanetCraft()
app.run()
