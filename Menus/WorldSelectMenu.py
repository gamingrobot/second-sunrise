from Menu import *


class WorldSelectMenu(Menu):
    def __init__(self, root, prevmenu):
        Menu.__init__(self, root, prevmenu, "Menus/worldSelectMenu.rml")

        #create events
        voxel = self.doc.GetElementById('voxel')
        voxel.AddEventListener('click', self.startVoxel, True)

        march = self.doc.GetElementById('march')
        march.AddEventListener('click', self.startMarch, True)

        back = self.doc.GetElementById('back')
        back.AddEventListener('click', self.goBackMenu, True)

    def startVoxel(self):
        self.startGame(voxel=True)

    def startMarch(self):
        self.startGame()

    def startGame(self, voxel=False):
        self.closeAllMenus()
        if voxel:
            self.root.startVoxel()
        else:
            self.root.startMarch()
