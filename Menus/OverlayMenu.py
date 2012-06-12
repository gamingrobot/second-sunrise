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

        pause = self.doc.GetElementById('pauseQuit')
        pause.AddEventListener('click', self.stop, True)

    def toggle(self):
        self.control.toggleOverlay()

    def stop(self):
        self.control.stop()
