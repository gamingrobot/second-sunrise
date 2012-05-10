#import sys
from Menu import *
#sys.path.insert(0, '..')
#from Controls import *

helper = None


class OverlayMenu(Menu):
    def __init__(self, mainControl):
        Menu.__init__(self, 'Menus/overlayMenu.rml')
        self.control = mainControl
        helper = self

    @staticmethod
    def resume():
        if helper != None:
            helper.toggle()
        else:
            print "Your worst fears have been realized"

    def toggle(self):
        self.control.toggleOverlay()
