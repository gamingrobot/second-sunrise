from panda3d.core import BitMask32
from panda3d.core import PointLight
from panda3d.core import VBase4


class Camera:
    """Does camera set up - will probably end up with lots of options."""
    def __init__(self, manager, xml):
        base.camNode.setCameraMask(BitMask32.bit(0))
        #base.disableMouse()
        self.reload(manager, xml)

    def reload(self, manager, xml):
        #only temporary while testing
        plight = PointLight('plight')
        bright = 2
        plight.setColor(VBase4(bright, bright, bright, 1))
        #plight.setAttenuation(Point3(0, 0, 0.5))
        plnp = base.camera.attachNewNode(plight)
        #plnp.setPos(0, 0, 0)
        render.setLight(plnp)

    def start(self):
        pass

    def stop(self):
        pass

    def destroy(self):
        pass
