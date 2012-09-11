from Menu import *


class WorldSelectMenu(Menu):
    def __init__(self, root, prevmenu):
        Menu.__init__(self, root, prevmenu, "Menus/worldSelectMenu.rml")

        #create events
        voxel = self.doc.GetElementById('voxel')
        voxel.AddEventListener('click', self.startVoxel, True)

        march = self.doc.GetElementById('march')
        march.AddEventListener('click', self.startMarch, True)

        net = self.doc.GetElementById('net')
        net.AddEventListener('click', self.startDualContour, True)

        back = self.doc.GetElementById('back')
        back.AddEventListener('click', self.goBackMenu, True)

    def startVoxel(self):
        self.closeAllMenus()
        self.root.startVoxel()

    def startMarch(self):
        self.closeAllMenus()
        self.root.startMarch()

    def startDualContour(self):
        self.closeAllMenus()
        self.root.startDualContour()
