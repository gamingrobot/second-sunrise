class Voxel:
    def __init__(self, chunk, size, chunks, pradius, noise, isovalue):
        self.blocks = chunk.blocks
        self.x = chunk.x
        self.y = chunk.y
        self.z = chunk.z
        self.size = size
        self.level = float(isovalue)
        self.triangles = []
        self.chunks = chunks
        self.radius = pradius
        self.noise = noise

    def generateMesh(self):
        for x in xrange(0, self.size):
            for y in xrange(0, self.size):
                for z in xrange(0, self.size):
                    block = self.blocks[x, y, z]
                    #current block exists
                    if not self.isEmptyBlock(block):
                        #left
                        block = None
                        if x >= 1:
                            block = self.blocks[x - 1, y, z]
                        if self.isEmptyBlock(block):
                            #self.triangles.append([[], [], []])
                            self.triangles.append([[x, y, z], [x, y, z + 1], [x, y + 1, z + 1]])
                            self.triangles.append([[x, y + 1, z + 1], [x, y + 1, z], [x, y, z]])
                        #front
                        block = None
                        if y >= 1:
                            block = self.blocks[x, y - 1, z]
                        if self.isEmptyBlock(block):
                            self.triangles.append([[x + 1, y, z], [x + 1, y, z + 1], [x, y, z + 1]])
                            self.triangles.append([[x, y, z + 1], [x, y, z], [x + 1, y, z]])
                        #right
                        block = None
                        if x < self.size - 1:
                            block = self.blocks[x + 1, y, z]
                        if self.isEmptyBlock(block):
                            self.triangles.append([[x + 1, y + 1, z + 1], [x + 1, y, z + 1], [x + 1, y, z]])
                            self.triangles.append([[x + 1, y, z], [x + 1, y + 1, z], [x + 1, y + 1, z + 1]])
                        #back
                        block = None
                        if y < self.size - 1:
                            block = self.blocks[x, y + 1, z]
                        if self.isEmptyBlock(block):
                            self.triangles.append([[x, y + 1, z + 1], [x + 1, y + 1, z + 1], [x + 1, y + 1, z]])
                            self.triangles.append([[x + 1, y + 1, z], [x, y + 1, z], [x, y + 1, z + 1]])
                        #bottom
                        block = None
                        if z > 1:
                            block = self.blocks[x, y, z - 1]
                        if self.isEmptyBlock(block):
                            self.triangles.append([[x, y + 1, z], [x + 1, y + 1, z], [x + 1, y, z]])
                            self.triangles.append([[x + 1, y, z], [x, y, z], [x, y + 1, z]])
                        #top
                        block = None
                        if z < self.size - 1:
                            block = self.blocks[x, y, z + 1]
                        if self.isEmptyBlock(block):
                            self.triangles.append([[x + 1, y, z + 1], [x + 1, y + 1, z + 1], [x, y + 1, z + 1]])
                            self.triangles.append([[x, y + 1, z + 1], [x, y, z + 1], [x + 1, y, z + 1]])
        return self.triangles

    def isEmptyBlock(self, block):
        if block == None or block.density < 0.0:
            return True
        else:
            return False
