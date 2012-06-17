from Menu import *


class OptionMenu(Menu):
    def __init__(self, root, prevmenu):
        Menu.__init__(self, root, prevmenu, "Menus/optionMenu.rml")

        #create events
        #remove this if/when forms work
        temp = self.doc.GetElementById('temp')
        temp.AddEventListener('click', self.goBackMenu, True)

        # read options here and set the appropriate elements
        #to the appropriate values

    # reads options from however they're stored - called by __init__
    def readOptions(self):
        pass
