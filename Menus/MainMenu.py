from Menu import *


class MainMenu(Menu):
    #will probably need an instance of Controls in here in the same way
    #OverlayMenu does
    def __init__(self, mainControl):
        print "hi"
        Menu.__init__(self, 'Menus/mainMenu.rml', 'mainMenu')
        self.doc.Show()

        self.controls = mainControl

        #get the play button and add a callback function for starting the game
        play = self.doc.GetElementById('play')
        play.AddEventListener('click', self.start, True)

        quit = self.doc.GetElementById('quit')
        quit.AddEventListener('click', self.stop, True)

    def start(self):
        #will have a multiPlay function eventually for multiplayer
        self.controls.singlePlay()

    def stop(self):
        self.controls.stop()
