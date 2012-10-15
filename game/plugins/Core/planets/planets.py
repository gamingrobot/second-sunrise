from panda3d.core import Point3
from planet import Planet


class Planets:
    """Well the Planets"""
    def __init__(self, manager, xml):
        self.reload(manager, xml)
        self.planets = {}

    def reload(self, manager, xml):
        chunks = xml.find('chunks')
        if chunks != None:
            self.chunks = manager.get(chunks.get('plugin'))
        else:
            self.chunks = None

    def start(self):
        pass

    def stop(self):
        pass

    def destroy(self):
        pass

    def makePlanet(self, cords, name, parentnode):
        self.planets[name] = Planet(cords, name, parentnode)
        self.chunks.makeChunk(Point3(0, 0, 0), self.planets[name].getNode(), name)
