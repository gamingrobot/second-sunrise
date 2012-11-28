from panda3d.core import Point3


class Universe:
    """That thing that came from the big bang"""
    def __init__(self, xml):
        self.reload(xml)

    def reload(self, xml):
        self.universeNode = render.attachNewNode("universe")
        planets = xml.find('planets')
        if planets != None:
            self.planets = manager.get(planets.get('plugin'))
        else:
            self.planets = None

        self.planets.makePlanet(Point3(0, 0, 0), "Gamma", self.universeNode)

        events.hookEvent("playerdeath", self.testcallback)

        manager.controls.registerKeyAll("Toggle Console", "F1", self.testcallback2, self)

    def start(self):
        pass

    def stop(self):
        self.universeNode.remove()

    def destroy(self):
        #self.universeNode.remove()
        pass

    def testcallback(self, event):
        log.info("Player died")

    def testcallback2(self):
        log.info("Key pressed")
