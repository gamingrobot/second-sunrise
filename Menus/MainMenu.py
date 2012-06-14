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
        play.AddEventListener('click', self.showPlayOpts, True)

        option = self.doc.GetElementById('options')
        option.AddEventListener('click', self.showOptions, True)

        quit = self.doc.GetElementById('quit')
        quit.AddEventListener('click', self.stop, True)

        #creates the option menu for starting the game
        self.startOpt = Menu('Menus/startOptMenu.rml', 'startOptMenu')

        voxel = self.startOpt.doc.GetElementById('voxel')
        voxel.AddEventListener('click', self.startVoxel, True)

        march = self.startOpt.doc.GetElementById('march')
        march.AddEventListener('click', self.startMarch, True)

        old = self.startOpt.doc.GetElementById('old')
        old.AddEventListener('click', self.start, True)

        back = self.startOpt.doc.GetElementById('back')
        back.AddEventListener('click', self.hidePlayOpts, True)

    def showOptions(self):
        self.optionMenu.show()
        self.doc.Hide()

    def showPlayOpts(self):
        self.startOpt.show()
        self.doc.Hide()

    def hidePlayOpts(self):
        self.doc.Show()
        self.startOpt.hide()

    #remove this method - temporary so game still works until seperated out
    #into voxel and marching cubes
    def start(self):
        self.startOpt.doc.Close()
        self.controls.singlePlay()

    def startVoxel(self):
        self.controls.app.startVoxel()

    def startMarch(self):
        self.controls.app.startMarch()

    def stop(self):
        self.controls.stop()
