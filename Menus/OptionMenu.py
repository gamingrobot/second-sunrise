from Menu import *


class OptionMenu(Menu):
    def __init__(self, root, prevmenu):
        Menu.__init__(self, root, prevmenu)

        self.musicButton = self.addButton(
            text = ("ToggleMusic"),  
            pos=(0,-0.3),
            command=self.toggleMusic
            )

        self.backButton = self.addButton(
            text = ("Back"),  
            pos=(0,-0.8),
            command=self.goBackMenu
            )

    # reads options from however they're stored - called by __init__
    def readOptions(self):
        pass

    def toggleMusic(self):
        self.root.toggleMusic()
        #Set musicbutton text here
