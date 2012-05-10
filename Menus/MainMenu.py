from Menu import *


class MainMenu(Menu):
    def __init__(self):
        print "hi"
        Menu.__init__(self, 'mainMenu.rml')
        self.doc.Show()
