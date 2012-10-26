from panda3d.core import Point3


class Universe:
    """That thing that came from the big bang"""
    def __init__(self, manager, xml):
        self.universeNode = render.attachNewNode("universe")
        self.reload(manager, xml)

    def reload(self, manager, xml):
        planets = xml.find('planets')
        if planets != None:
            self.planets = manager.get(planets.get('plugin'))
        else:
            self.planets = None

        self.planets.makePlanet(Point3(0, 0, 0), "Gamma", self.universeNode)

        eventmg = manager.get("events")
        eventmg.hookEvent("playerdeath", self.testcallback)

        #controlsmg = manager.get("controls")
        #controlsmg.registerKeyGame("Toggle Console", "F1", self.testcallback2, self.__class__.__name__)

    def start(self):
        pass

    def stop(self):
        pass

    def destroy(self):
        self.universeNode.remove()

    def testcallback(self, event):
        print "Player died"

    def testcallback2(self):
        print "Key pressed"
