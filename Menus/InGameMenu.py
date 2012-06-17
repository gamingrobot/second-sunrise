from Menu import *
from OptionMenu import *


class InGameMenu(Menu):
    def __init__(self, root, player):
        Menu.__init__(self, root, None, "Menus/inGameMenu.rml")
        self.player = player

        el = self.doc.GetElementById('resume')
        el.AddEventListener('click', self.toggle, True)

        pause = self.doc.GetElementById('pauseQuit')
        pause.AddEventListener('click', self.stop, True)

        option = self.doc.GetElementById('options')
        option.AddEventListener('click', self.ShowOptions, True)

    def ShowOptions(self):
        self.optionMenu = OptionMenu(self.root, self)
        self.goToMenu(self.optionMenu)

    def toggle(self):
        self.player.toggleInGameMenu()

    def stop(self):
        self.player.stop()
