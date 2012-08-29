from Menu import *


class ConsoleMenu(Menu):
    def __init__(self, root, prevmenu):
        Menu.__init__(self, root, prevmenu, "Menus/consoleMenu.rml")

        self.input = self.doc.GetElementById('input')
        self.input.AddEventListener('textinput', self.inputKeyDown, True)

    def inputKeyDown(self):
        print "INPUTTEXT"
