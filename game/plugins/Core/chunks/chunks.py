from pchunk import PChunk as Chunk
from panda3d.core import Point3


class Chunks:
    """Chunk class manages the creation of chunks"""
    def __init__(self, manager, xml):
        self.reload(manager, xml)
        self.chunks = {}
        self.chunksize = 16

    def reload(self, manager, xml):
        meshgen = xml.find('meshgen')
        if meshgen != None:
            print "DEBUG: " + meshgen.get('plugin')
            self.meshgen = manager.get(meshgen.get('plugin'))
        else:
            self.meshgen = None
        terraingen = xml.find('terraingen')
        if terraingen != None:
            print "DEBUG: " + terraingen.get('plugin')
            self.terraingen = manager.get(terraingen.get('plugin'))
        else:
            self.terraingen = None

    def start(self):
        pass

    def stop(self):
        pass

    def destroy(self):
        pass

    def makeChunk(self, chunkcords, parentnode, planetname):
        if not planetname in self.chunks:
            self.chunks[planetname] = {}
        #make chunk
        self.chunks[planetname][chunkcords] = Chunk(chunkcords, chunkcords * self.chunksize)
        #create chunk
        self.generateChunk(chunkcords, parentnode, self.chunks[planetname])
        #regen all negative neighbors
        #get negative neighbors
        neighbors = self.getNegativeNeighbors(chunkcords, self.chunks[planetname])
        for neighbor in neighbors:
            if neighbor != None:
                self.generateChunk(neighbor, parentnode, self.chunks[planetname])

    def generateChunk(self, chunkcords, parentnode, chunks):
        chunk = chunks[chunkcords]
        print "Generating: " + str(chunk.cords[0]) + "," + str(chunk.cords[1]) + "," + str(chunk.cords[2])
        #generate terrain
        chunk.setTerrain(self.terraingen.generate(chunk.abscords, self.chunksize))
        #build list of neighbors
        terrain = self.getNeighbors(chunk.cords, chunks)
        #generate mesh
        chunk.setMesh(self.meshgen.generate(terrain, self.chunksize, lod=1.0))
        #remove old node if exists
        try:
            chunk.getNode().removeNode()
            chunk.setNode(None)
            print "Removed old node"
        except AttributeError:
            pass
        #add to render
        chunk.setNode(parentnode.attachNewNode(chunk.getMesh()))
        chunk.getNode().setPos(chunk.abscords)
        chunk.getNode().setTag('Pickable', '1')

    def getNeighbors(self, cords, chunks):
        terrain = [None for i in range(8)]
        x, y, z = cords[0], cords[1], cords[2]
        terrain[0] = chunks[Point3(x, y, z)].getTerrain()
        point = Point3(x + 1, y + 1, z + 1)
        if point in chunks:
            terrain[1] = chunks[point].getTerrain()
        point = Point3(x + 1, y + 1, z)
        if point in chunks:
            terrain[2] = chunks[point].getTerrain()
        point = Point3(x + 1, y, z + 1)
        if point in chunks:
            terrain[3] = chunks[point].getTerrain()
        point = Point3(x, y + 1, z + 1)
        if point in chunks:
            terrain[4] = chunks[point].getTerrain()
        point = Point3(x + 1, y, z)
        if point in chunks:
            terrain[5] = chunks[point].getTerrain()
        point = Point3(x, y + 1, z)
        if point in chunks:
            terrain[6] = chunks[point].getTerrain()
        point = Point3(x, y, z + 1)
        if point in chunks:
            terrain[7] = chunks[point].getTerrain()
        return terrain

    def getNegativeNeighbors(self, cords, chunks):
        neighbors = [None for i in range(7)]
        x, y, z = cords[0], cords[1], cords[2]
        point = Point3(x - 1, y - 1, z - 1)
        if point in chunks:
            neighbors[0] = point
        point = Point3(x - 1, y - 1, z)
        if point in chunks:
            neighbors[1] = point
        point = Point3(x - 1, y, z - 1)
        if point in chunks:
            neighbors[2] = point
        point = Point3(x, y - 1, z - 1)
        if point in chunks:
            neighbors[3] = point
        point = Point3(x - 1, y, z)
        if point in chunks:
            neighbors[4] = point
        point = Point3(x, y - 1, z)
        if point in chunks:
            neighbors[5] = point
        point = Point3(x, y, z - 1)
        if point in chunks:
            neighbors[6] = point
        return neighbors
