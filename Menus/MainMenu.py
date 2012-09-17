from Menu import *
from OptionMenu import *
from WorldSelectMenu import *
from ConsoleMenu import *
from direct.gui.DirectGui import *


class MainMenu(Menu):
    def __init__(self, root, prevmenu):
        Menu.__init__(self, root, prevmenu)

        #DirectGui
        self.playButton = self.addButton(
            text = ("Play", "Games", "Alot"),  
            pos=(0,0.6),
            command=self.ShowWorldMenu
            )

        self.optionsButton = self.addButton(
            text = ("Options"),  
            pos=(0,0.1),
            command=self.ShowOptions
            )

        self.consoleButton = self.addButton(
            text = ("Console"),  
            pos=(0,-0.4),
            command=self.ShowConsole
            )

        self.quitButton = self.addButton(
            text = ("Quit"),  
            pos=(0,-0.8),
            command=self.stop
            )

    def ShowOptions(self):
        #could also create it here, just a matter of performance
        #self.optionMenu = OptionMenu(self.root, self)
        optionMenu = OptionMenu(self.root, self)
        self.goToMenu(optionMenu)

    def ShowWorldMenu(self):
        worldSelectMenu = WorldSelectMenu(self.root, self)
        self.goToMenu(worldSelectMenu)

    def ShowConsole(self):
        consoleMenu = ConsoleMenu(self.root, self)
        self.goToMenu(consoleMenu)

    def stop(self):
        self.root.stop()
