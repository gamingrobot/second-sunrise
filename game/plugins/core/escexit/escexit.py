from direct.showbase import DirectObject


class EscExit(DirectObject.DirectObject):
    """This arranges it so that the escape key causes the program to instantly exit. Note that it disables this feature during a transition - this is required otherwise this object could never be deleted."""
    """TODO: fix with register control"""
    def __init__(self, manager, xml):
        self.end = manager.end
        controlsmg = manager.get("controls")
        controlsmg.registerKeyGame("Excape Game", "escape", self.end, self.__class__.__name__)

    def reload(self, manager, xml):
        pass

    def start(self):
        pass

    def stop(self):
        #self.ignore('escape')
        pass

    def destroy(self):
        pass
