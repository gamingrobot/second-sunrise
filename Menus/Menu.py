from panda3d.rocket import *


class Menu:
    def __init__(self,  root, prevmenu, rmlpath):
        self.root = root
        self.prevmenu = prevmenu
        #create menu
        self.doc = self.root.rocketContext.LoadDocument(rmlpath)

    def goBackMenu(self):
        self.prevmenu.doc.Show()
        self.doc.Hide()

    def goToMenu(self, themenu):
        self.doc.Hide()
        themenu.doc.Show()

    def closeAllMenus(self):
        if self.prevmenu != None:
            self.prevmenu.closeAllMenus()
        self.closeMenu()

    def closeMenu(self):
        self.doc.Close()
