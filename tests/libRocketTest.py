#!/usr/bin/env python
from direct.showbase.ShowBase import ShowBase
from panda3d.rocket import *


class rocketTest(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.ovrlay = False
        #self.r = RocketRegion.make('pandaRocket', base.win)
        #self.r.setActive(1)
        #self.context = self.r.getContext()
        #self.rWin = self.context.LoadDocument('rocketTest.rml')

        LoadFontFace("rocket-sample/assets/Delicious-Roman.otf")

        r = RocketRegion.make('pandaRocket', base.win)
        r.setActive(1)
        context = r.getContext()

        #context.LoadDocument('rocket-sample/data/background.rml').Show()

        self.doc = context.LoadDocument('rocketTest.rml')
        #doc.Show()

        ih = RocketInputHandler()
        base.mouseWatcher.attachNewNode(ih)
        r.setInputHandler(ih)

        self.accept("escape", self.overlay)

    def overlay(self):
        self.ovrlay = not self.ovrlay

        if (self.ovrlay):
            self.doc.Show()
        else:
            self.doc.Hide()

app = rocketTest()

#def test():
#    app.overlay()

#app.doc.GetElementById('resume').AddEventListener("click", "test()", True)
app.run()
