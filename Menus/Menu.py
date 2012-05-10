from panda3d.rocket import *


class Menu:
    def __init__(self, fname, regionName):
        LoadFontFace("tests/rocket-sample/assets/Delicious-Roman.otf")

        self.r = RocketRegion.make(regionName, base.win)
        self.r.setActive(1)
        self.context = self.r.getContext()

        self.doc = self.context.LoadDocument(fname)

        self.ih = RocketInputHandler()
        base.mouseWatcher.attachNewNode(self.ih)
        self.r.setInputHandler(self.ih)

    def show(self):
        self.doc.Show()

    def hide(self):
        self.doc.Hide()
