from Menu import *
from OptionMenu import *


class InGameMenu(Menu):
    def __init__(self, root, player):
        Menu.__init__(self, root, None)
        self.player = player

        self.resumeButton = self.addButton(
            text = ("Resume"),  
            pos=(0,-0.8),
            command=self.toggle
            )

        self.quitButton = self.addButton(
            text = ("Quit"),  
            pos=(0,-0.8),
            command=self.stop
            )

        self.optionsButton = self.addButton(
            text = ("Options"),  
            pos=(0,-0.8),
            command=self.ShowOptions
            )

        self.mainFrame.hide()

    def ShowOptions(self):
        optionMenu = OptionMenu(self.root, self)
        self.goToMenu(optionMenu)

    def toggle(self):
        self.player.toggleInGameMenu()

    def stop(self):
        self.player.stop()
