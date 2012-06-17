from Menu import *
from OptionMenu import *
from WorldSelectMenu import *


class MainMenu(Menu):
    def __init__(self, root, prevmenu):
        Menu.__init__(self, root, prevmenu, "Menus/mainMenu.rml")

        #can create options menu here
        #create options menu (root, currentmenu)
        self.optionMenu = OptionMenu(self.root, self)

        #create world menu (root, currentmenu)
        self.worldSelectMenu = WorldSelectMenu(self.root, self)

        #get the play button and add a callback function for starting the game
        play = self.doc.GetElementById('play')
        play.AddEventListener('click', self.ShowWorldMenu, True)

        option = self.doc.GetElementById('options')
        option.AddEventListener('click', self.ShowOptions, True)

        quit = self.doc.GetElementById('quit')
        quit.AddEventListener('click', self.stop, True)

    def ShowOptions(self):
        #could also create it here, just a matter of performance
        #self.optionMenu = OptionMenu(self.root, self)
        self.goToMenu(self.optionMenu)

    def ShowWorldMenu(self):
        self.goToMenu(self.worldSelectMenu)

    def stop(self):
        pass
        #self.root.stop()
