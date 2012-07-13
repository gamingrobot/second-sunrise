# UTITLTY CLASS USED FOR ODD FUNCTION
import math


def getDensity(chunkcords, blockcords, radius, noise):
    ab = math.fabs
    x, y, z = chunkcords[0] + blockcords[0], chunkcords[1] + blockcords[1], chunkcords[2] + blockcords[2]

    #if math.sqrt((ab(x)) ** 2 + (ab(y)) ** 2 + (ab(z)) ** 2) <= self.radius:
    #if noise.noise(x, y, z) >= 0.0:
    #    return float(1.0)
    #else:
    #    return float(-1.0)

    value = 0
    #for i in xrange(1):
    #    value += noise.noise(x * 2 ** i, y * 2 ** i, z * 2 ** i)
    value += octave(x, y, z, 1.0, noise)
    value += octave(x, y, z, 2.0, noise)
    return value


def octave(x, y, z, octa, noise):
    return (1.0 / octa) * noise.noise(x * octa, y * octa, z * octa)


def genHash(self, x, y, z):
    return str(x) + ":" + str(y) + ":" + str(z)
