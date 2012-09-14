from panda3d.rocket import *
from direct.gui.DirectGui import *


class Hud:
    def __init__(self, root):
        self.root = root
        self.mainFrame = DirectFrame(frameColor=(0,0,0,0))

