# UTITLTY CLASS USED FOR ODD FUNCTION
import math


def getDensity(chunkcords, blockcords, radius):
    ab = math.fabs
    if math.sqrt((ab(chunkcords[0] + blockcords[0])) ** 2 + (ab(chunkcords[1] + blockcords[1])) ** 2 + (ab(chunkcords[2] + blockcords[2])) ** 2) <= radius:
        return float(1.0)
    else:
        return float(-1.0)


def genHash(self, x, y, z):
    return str(x) + ":" + str(y) + ":" + str(z)
