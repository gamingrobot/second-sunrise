# UTITLTY CLASS USED FOR ODD FUNCTION
import math


def getDensity(chunkcords, blockcords, radius, noise):
    ab = math.fabs
    #x, y, z = chunkcords[0] + blockcords[0], chunkcords[1] + blockcords[1], chunkcords[2] + blockcords[2]

    #if math.sqrt((ab(x)) ** 2 + (ab(y)) ** 2 + (ab(z)) ** 2) <= self.radius:
    #if noise.noise(x, y, z) >= 0.0:
    #    return float(1.0)
    #else:
    #    return float(-1.0)

    #RAVINES
    x, y, z = blockcords[0], blockcords[1], blockcords[2]
    cx, cy, cz = chunkcords[0], chunkcords[1], chunkcords[2]
    #noise.setScale(15)
    density = 0.1 - 2 * ((z + cz) / 128)
    density += octave((x + cx), (y + cy), (z + cz), 3, noise)
    density += noise.noise((x + cx), (y + cy), (z + cz))

    return density


def octave(x, y, z, octa, noise):
    return (2.0 / octa) * noise.noise(x * octa, y * octa, z * octa)


def genHash(self, x, y, z):
    return str(x) + ":" + str(y) + ":" + str(z)
