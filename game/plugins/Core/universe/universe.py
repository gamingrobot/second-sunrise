from panda3d.core import Vec3


class Universe:
    """That thing that came from the big bang"""
    def __init__(self, manager, xml):
        self.reload(manager, xml)
        self.universeNode = render.attachNewNode("universe")

    def reload(self, manager, xml):
        planets = xml.find('planets')
        if planets != None:
            self.planets = manager.get(planets.get('plugin'))
        else:
            self.planets = None

    def start(self):
        self.planets.makePlanet(Vec3(0, 0, 0), "Gamma", self.universeNode)

    def stop(self):
        pass

    def destroy(self):
        pass
