from direct.showbase import DirectObject


class FrameRate(DirectObject.DirectObject):
    """Toggles displaying the framerate"""
    """TODO: fix with register control"""
    def __init__(self, manager, xml):
        self.state = False

    def reload(self, manager, xml):
        pass

    def start(self):
        self.accept('f12', self.toggle)

    def stop(self):
        self.ignore('f12')

    def destroy(self):
        pass

    def toggle(self):
        self.state = not self.state
        base.setFrameRateMeter(self.state)
