import numpy as np
from panda3d.core import Point3


class TerrainGeneration:
    """Terraingeneration for the chunks"""
    def __init__(self, xml):
        self.reload(xml)
        self.isovalue = 0.0

    def reload(self, xml):
        noise = xml.find('noise')
        if noise != None:
            log.debug(noise.get('plugin'))
            self.noise = manager.get(noise.get('plugin'))
        else:
            self.noise = None

    def start(self):
        pass

    def stop(self):
        pass

    def destroy(self):
        pass

    def generate(self, startcords, size):
        blocks = np.zeros((size, size, size), dtype=np.object)
        #init numpy
        it = np.nditer(blocks, op_flags=['readwrite'], flags=['multi_index', 'refs_ok'])
        while not it.finished:
            index = it.multi_index
            den = self.noise.getDensity(startcords + Point3(index[0], index[1], index[2]))
            if den >= self.isovalue:
                #blockid, density
                it[0] = [[1, den]]
            else:
                #blockid, density
                it[0] = [[0, den]]
            it.iternext()
        return blocks
