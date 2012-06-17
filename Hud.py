from panda3d.rocket import *


class Hud:
    def __init__(self, root):
        self.root = root
        self.doc = self.root.rocketContext.LoadDocument("hud.rml")
        self.doc.Show()
