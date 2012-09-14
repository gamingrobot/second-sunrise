from panda3d.rocket import *
from direct.gui.DirectGui import *


class Menu:
    def __init__(self,  root, prevmenu):
        self.root = root
        self.prevmenu = prevmenu
        #create menu
        self.mainFrame = DirectFrame(frameColor=(0,0,0,0))

    def goBackMenu(self):
        self.prevmenu.mainFrame.show()
        self.closeMenu()

    def goToMenu(self, themenu):
        self.mainFrame.hide()
        themenu.mainFrame.show()

    def closeAllMenus(self):
        if self.prevmenu != None:
            self.prevmenu.closeAllMenus()
        self.closeMenu()

    def closeMenu(self):
        self.mainFrame.destroy()


    def addButton(self, text=(""), pos=(0,0), command=None):
        self.abutton = DirectButton(
            text=text,  
            pos=(pos[0], 0, pos[1]),
            scale=0.2,
            frameColor=(0,0,1,1),
            command=command
            )
        self.abutton.reparentTo(self.mainFrame)
