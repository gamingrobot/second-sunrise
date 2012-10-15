from pchunk import PChunk as Chunk


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
        self.chunks[planetname] = []
        #create chunk
        self.chunks[planetname].append(Chunk(chunkcords, chunkcords * self.chunksize))
        for chunk in self.chunks[planetname]:
            print chunk.cords
            #generate terrain
            chunk.setTerrain(self.terraingen.generate(chunk.abscords, self.chunksize))
            #generate mesh for now it passes one terrain block, but it will soon be a list of 8, the current and all positive neighbors
            #chunk.setMesh(self.meshgen.generate(chunk.getTerrain(), self.chunksize, lod=1.0))
            #add to render
            #chunk.setNode(parentnode.attachNewNode(chunk.getMesh()))
            #chunk.getNode.setPos(chunk.abscords)
            #chunk.getNode.setTag('Pickable', '1')
