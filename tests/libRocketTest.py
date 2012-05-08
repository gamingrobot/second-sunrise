#!/usr/bin/env python
from direct.showbase.ShowBase import ShowBase
from panda3d.rocket import *


class rocketTest(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.ovrlay = False
        self.r = RocketRegion.make('pandaRocket', base.win)
        self.r.setActive(1)
        self.context = self.r.getContext()
        self.rWin = self.context.LoadDocument('rocketTest.rml')

        self.accept("escape", self.overlay)

    def overlay(self):
        self.ovrlay = not self.ovrlay

        if (self.ovrlay):
            print "Overlay enabled"
            self.rWin.Show()
        else:
            print "Overlay disabled"

app = rocketTest()
app.run()
