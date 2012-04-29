#Chunk.py

import Space

class Chunk:
    """Chunk contains 32x32x32 blocks"""
    def __init__(self):
        self.blocks = [][][]    #this is apparently an error
        for x in xrange(0,32):
            for y in range(0, 32):
                for z in range(0, 32):
                    self.blocks[x][y][z] = Space()
