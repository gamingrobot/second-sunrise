from direct.showbase import DirectObject


class EscExit(DirectObject.DirectObject):
    """This arranges it so that the escape key causes the program to instantly exit. Note that it disables this feature during a transition - this is required otherwise this object could never be deleted."""
    """TODO: fix with register control"""
    def __init__(self, xml):
        self.end = manager.end
        #controls = manager.get("controls")
        #controls.registerKeyGame("Excape Game", "escape", self.end, self)
        #controls.registerKeyMenu("Excape Game", "escape", self.end, self)

    def reload(self, xml):
        pass

    def start(self):
        pass

    def stop(self):
        #self.ignore('escape')
        pass

    def destroy(self):
        pass
