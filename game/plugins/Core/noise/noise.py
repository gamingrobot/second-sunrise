from simplexnoise import *


class Noise:
    """MeshGenerators for the chunks"""
    def __init__(self, manager, xml):
        self.reload(manager, xml)

    def reload(self, manager, xml):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def destroy(self):
        pass

    def getDensity(self, cords, getDer=False):
        #return 1.0
        x, y, z = cords[0], cords[1], cords[2]
        den, der = raw_noise_3d(x / 15.0, y / 15.0, z / 15.0)
        if getDer:
            return den, der
        else:
            return den
