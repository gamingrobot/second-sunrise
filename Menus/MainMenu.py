from Menu import *


class MainMenu(Menu):
    #will probably need an instance of Controls in here in the same way
    #OverlayMenu does
    def __init__(self):
        print "hi"
        Menu.__init__(self, 'Menus/mainMenu.rml', 'mainMenu')
        self.doc.Show()
