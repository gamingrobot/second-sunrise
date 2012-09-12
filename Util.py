# UTITLTY CLASS USED FOR ODD FUNCTION
import math
from simplexnoise import *


class MeshType:
    Voxel = 0
    MarchingCubes = 1
    DualContour = 2


def getDensity(chunkcords, blockcords, radius, noise, getDer=False):
    """ab = math.fabs
    x, y, z = chunkcords[0] + blockcords[0], chunkcords[1] + blockcords[1], chunkcords[2] + blockcords[2]

    #if math.sqrt((ab(x)) ** 2 + (ab(y)) ** 2 + (ab(z)) ** 2) <= self.radius:
    #if noise.noise(x, y, z) >= 0.0:
    #    return float(1.0)
    #else:
    #    return float(-1.0)

    #4:16 PM - Nissehutt: int yMin = (int) (maxblock.Y - (NoiseGenerator.Noise( x, z ) * (2 * defaultSizeOfBlock)));

    #x, y, z = blockcords[0], blockcords[1], blockcords[2]
    noise.setScale(60)

    TopGenerate = 128
    GenerateDepth = 64
    NoiseZ = noise(x, y)
    NoiseZ += 1.0
    NoiseZ *= 0.5

    Depth = TopGenerate - (NoiseZ * GenerateDepth)
    #print Depth

    if z < round(Depth):
        ret = (Depth - int(Depth))
        return ret
    else:
        ret = (Depth - int(Depth)) * -1
        return ret"""

    #SetBlocksInVolume(x, TopGenerate, z, x, Depth, z)
    """public static void GenerateTerrainOnBlock(int x, int z)
    {
        const int TopGenerate = 256, GenerateDepth = 128, Water = 150;

        double NoiseY = CreateNoise(x, y);

        int Depth = TopGenerate - (int)(NoiseY * GenerateDepth);

        SetBlocksInVolume(x, TopGenerate, z, x, Depth, z);
    }

    public static void SetBlocksInVolume(int frX, int frY, int frZ, int toX, int toY, int toZ, Material material){
        //Set blocks here in whatever way you do set blocks
    }"""
    #print density
    """#RAVINES
    x, y, z = blockcords[0], blockcords[1], blockcords[2]
    cx, cy, cz = chunkcords[0], chunkcords[1], chunkcords[2]
    #noise.setScale(15)
    density = 0.1 - 2 * ((z + cz) / 128)
    density += octave((x + cx), (y + cy), (z + cz), 3, noise)
    density += noise.noise((x + cx), (y + cy), (z + cz))
    return density"""
    """x, y, z = chunkcords[0] + blockcords[0], chunkcords[1] + blockcords[1], chunkcords[2] + blockcords[2]
    scale = 100.0
    hiBound = 30
    loBound = -5
    imp = [x / scale, y / scale, z / scale]
    den = scaled_raw_noise(-5, 30, x/100.0, y/100.0, z/100.0)
    return den"""
    """x, y, z = chunkcords[0] + blockcords[0], chunkcords[1] + blockcords[1], chunkcords[2] + blockcords[2]
    noise.setScale(1)
    scale = 15.0
    print x, y, z
    print x / scale, y / scale, z / scale
    den = noise.noise(x / scale, y / scale, z / scale)
    print den
    return den"""
    x, y, z = chunkcords[0] + blockcords[0], chunkcords[1] + blockcords[1], chunkcords[2] + blockcords[2]
    den, der = raw_noise_3d(x/15.0, y/15.0, z/15.0)
    if getDer:
        return den, der
    else:
        return den


def octave(x, y, z, octa, noise):
    return (2.0 / octa) * noise.noise(x * octa, y * octa, z * octa)


def genHash(x, y, z):
    return str(x) + ":" + str(y) + ":" + str(z)
