from Menu import *


class WorldSelectMenu(Menu):
    def __init__(self, root, prevmenu):
        Menu.__init__(self, root, prevmenu)

        #DirectGui
        self.playButton = self.addButton(
            text = ("Voxel"),  
            pos=(0,0.6),
            command=self.startVoxel
            )

        self.optionsButton = self.addButton(
            text = ("Marching Cubes"),  
            pos=(0,0.1),
            command=self.startMarch
            )

        self.consoleButton = self.addButton(
            text = ("Dual Contour"),  
            pos=(0,-0.4),
            command=self.startDualContour
            )

        self.quitButton = self.addButton(
            text = ("Back"),  
            pos=(0,-0.8),
            command=self.goBackMenu
            )

    def startVoxel(self):
        self.closeAllMenus()
        self.root.startVoxel()

    def startMarch(self):
        self.closeAllMenus()
        self.root.startMarch()

    def startDualContour(self):
        self.closeAllMenus()
        self.root.startDualContour()
