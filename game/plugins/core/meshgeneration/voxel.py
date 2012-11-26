from bin.shared import myiter


class Voxel:
    def __init__(self):
        self.isovalue = 0.0

    def generateMesh(self, terrain, size, lod):
        triangles = []
        for x, y, z in myiter.product(xrange(0, size), xrange(0, size), xrange(0, size)):
            block = terrain[0][x, y, z]
            #current block exists
            if not self.isEmptyBlock(block):
                #left
                block = None
                if x >= 1:
                    block = terrain[0][x - 1, y, z]
                if self.isEmptyBlock(block):
                    #triangles.append([[], [], []])
                    triangles.append([[x, y, z], [x, y, z + 1], [x, y + 1, z + 1]])
                    triangles.append([[x, y + 1, z + 1], [x, y + 1, z], [x, y, z]])
                #front
                block = None
                if y >= 1:
                    block = terrain[0][x, y - 1, z]
                if self.isEmptyBlock(block):
                    triangles.append([[x + 1, y, z], [x + 1, y, z + 1], [x, y, z + 1]])
                    triangles.append([[x, y, z + 1], [x, y, z], [x + 1, y, z]])
                #right
                block = None
                if x < size - 1:
                    block = terrain[0][x + 1, y, z]
                if self.isEmptyBlock(block):
                    triangles.append([[x + 1, y + 1, z + 1], [x + 1, y, z + 1], [x + 1, y, z]])
                    triangles.append([[x + 1, y, z], [x + 1, y + 1, z], [x + 1, y + 1, z + 1]])
                #back
                block = None
                if y < size - 1:
                    block = terrain[0][x, y + 1, z]
                if self.isEmptyBlock(block):
                    triangles.append([[x, y + 1, z + 1], [x + 1, y + 1, z + 1], [x + 1, y + 1, z]])
                    triangles.append([[x + 1, y + 1, z], [x, y + 1, z], [x, y + 1, z + 1]])
                #bottom
                block = None
                if z > 1:
                    block = terrain[0][x, y, z - 1]
                if self.isEmptyBlock(block):
                    triangles.append([[x, y + 1, z], [x + 1, y + 1, z], [x + 1, y, z]])
                    triangles.append([[x + 1, y, z], [x, y, z], [x, y + 1, z]])
                #top
                block = None
                if z < size - 1:
                    block = terrain[0][x, y, z + 1]
                if self.isEmptyBlock(block):
                    triangles.append([[x + 1, y, z + 1], [x + 1, y + 1, z + 1], [x, y + 1, z + 1]])
                    triangles.append([[x, y + 1, z + 1], [x, y, z + 1], [x + 1, y, z + 1]])
        return triangles

    def isEmptyBlock(self, block):
        if block == None or block[1] < self.isovalue:
            return True
        else:
            return False
