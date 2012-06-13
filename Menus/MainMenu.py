from Menu import *
from OptionMenu import *


class MainMenu(Menu):
    def __init__(self, mainControl):
        print "hi"
        Menu.__init__(self, 'Menus/mainMenu.rml', 'mainMenu')
        #self.doc.Show()
        self.show()

        self.controls = mainControl

        self.optionMenu = OptionMenu(self)

        #get the play button and add a callback function for starting the game
        play = self.doc.GetElementById('play')
        play.AddEventListener('click', self.start, True)

        option = self.doc.GetElementById('options')
        option.AddEventListener('click', self.showOptions, True)

        quit = self.doc.GetElementById('quit')
        quit.AddEventListener('click', self.stop, True)

    def showOptions(self):
        self.doc.Hide()
        self.optionMenu.show()

    def start(self):
        #will have a multiPlay function eventually for multiplayer
        self.controls.singlePlay()

    def stop(self):
        self.controls.stop()
