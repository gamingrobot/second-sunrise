from Menu import *


class OptionMenu(Menu):
    def __init__(self, returnMenu):
        Menu.__init__(self, 'Menus/optionSheet.rml', 'optionMenu')

        self.retMenu = returnMenu

        #form = self.doc.GetElementById('options')
        #form.AddEventListener('submit', self.saveOptions, True)

        #remove this if/when forms work
        temp = self.doc.GetElementById('temp')
        temp.AddEventListener('click', self.saveOptions, True)

        # read options here and set the appropriate elements
        #to the appropriate values

    # form processor - saves options
    def saveOptions(self):
        self.retMenu.show()
        self.doc.Hide()

    # reads options from however they're stored - called by __init__
    def readOptions(self):
        pass
