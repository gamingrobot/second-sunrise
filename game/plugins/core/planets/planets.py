from panda3d.core import Point3
import math
from planet import Planet


class Planets:
    """Well the Planets"""
    def __init__(self, xml):
        self.reload(xml)
        self.planets = {}
        events.hookEvent("playermove", self.playerMoved)
        events.hookEvent("playerspawn", self.playerMoved)

    def reload(self, xml):
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

    def playerMoved(self, eventdata):
        #TODO: fix later but for now its a bounding box and not a sphere
        #could use bullet ghosts to see if player is in the planet but may be slow
        #TODO: fix so cords are better currently just rough
        for name in self.planets:
            player = eventdata
            #log.debug("player is at", player)
            #log.debug("checking if player is in:", name)
            planetborder = self.planets[name].psize * self.chunks.chunksize
            positiveborder = self.planets[name].cords + planetborder
            negtiveborder = self.planets[name].cords - planetborder
            #check for a fail case
            #log.debug(player.x, player.y, player.z)
            if (player.x < positiveborder.x and player.x > negtiveborder.x) and (player.y < positiveborder.y and player.y > negtiveborder.y) and (player.z < positiveborder.z and player.z > negtiveborder.z):
                #log.info("player is in planet", name)
                #move cords to 0,0,0 for player
                playercords = player - self.planets[name].cords
                chunkfloat = playercords / self.chunks.chunksize
                playerchunk = Point3(math.floor(chunkfloat[0]), math.floor(chunkfloat[1]), math.floor(chunkfloat[2]))
                #log.info("player is in chunk:", playerchunk)

                self.generatePlusChunks(playerchunk, name)
                break
            else:
                log.info("player is NOT in planet", name)

    def makePlanet(self, cords, radius, name, parentnode):
        self.planets[name] = Planet(cords, radius, name, parentnode)
        #self.generatePositiveChunks(Point3(-1, -1, -1), name)
        #self.generatePlusChunks(Point3(0, 0, 0), name)
        #spawn player here

    def generatePlusChunks(self, point, name):
        #main chunk first but for speed its in the middle
        #self.chunks.makeChunk(point + Point3(0, 0, 0), self.planets[name].getNode(), name)
        #rest of plus sign
        self.chunks.makeChunk(point + Point3(1, 0, 0), self.planets[name].getNode(), name)
        self.chunks.makeChunk(point + Point3(0, 1, 0), self.planets[name].getNode(), name)
        self.chunks.makeChunk(point + Point3(0, 0, 1), self.planets[name].getNode(), name)
        self.chunks.makeChunk(point + Point3(0, 0, 0), self.planets[name].getNode(), name)
        self.chunks.makeChunk(point + Point3(-1, 0, 0), self.planets[name].getNode(), name)
        self.chunks.makeChunk(point + Point3(0, -1, 0), self.planets[name].getNode(), name)
        self.chunks.makeChunk(point + Point3(0, 0, -1), self.planets[name].getNode(), name)

    def generatePositiveChunks(self, point, name):
        self.chunks.makeChunk(point + Point3(1, 1, 1), self.planets[name].getNode(), name)
        self.chunks.makeChunk(point + Point3(1, 1, 0), self.planets[name].getNode(), name)
        self.chunks.makeChunk(point + Point3(1, 0, 1), self.planets[name].getNode(), name)
        self.chunks.makeChunk(point + Point3(0, 1, 1), self.planets[name].getNode(), name)
        self.chunks.makeChunk(point + Point3(1, 0, 0), self.planets[name].getNode(), name)
        self.chunks.makeChunk(point + Point3(0, 1, 0), self.planets[name].getNode(), name)
        self.chunks.makeChunk(point + Point3(0, 0, 1), self.planets[name].getNode(), name)
        self.chunks.makeChunk(point + Point3(0, 0, 0), self.planets[name].getNode(), name)
