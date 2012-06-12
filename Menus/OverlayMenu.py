#import sys
from Menu import *
#sys.path.insert(0, '..')
#from Controls import *


class OverlayMenu(Menu):
    def __init__(self, mainControl):
        Menu.__init__(self, 'Menus/overlayMenu.rml', 'overlayMenu')
        self.control = mainControl

        el = self.doc.GetElementById('resume')
        el.AddEventListener('click', self.toggle, True)

    def toggle(self):
        self.control.toggleOverlay()
