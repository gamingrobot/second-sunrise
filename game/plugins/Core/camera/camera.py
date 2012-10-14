from panda3d.core import BitMask32


class Camera:
    """Does camera set up - will probably end up with lots of options."""
    def __init__(self, manager, xml):
        base.camNode.setCameraMask(BitMask32.bit(0))
        base.disableMouse()
        self.reload(manager, xml)

    def reload(self, manager, xml):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def destroy(self):
        pass
