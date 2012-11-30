from simplexnoise import *


class Noise:
    """MeshGenerators for the chunks"""
    def __init__(self, xml):
        self.reload(xml)

    def reload(self, xml):
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
        den, der = raw_noise_3d(x / 100.0, y / 100.0, z / 100.0)
        if getDer:
            return den, der
        else:
            return den
