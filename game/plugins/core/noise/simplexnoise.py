import math


def raw_noise_3d(x, y, z):
    """3D Raw Simplex noise."""
    # Noise contributions from the four corners
    n0, n1, n2, n3 = 0.0, 0.0, 0.0, 0.0

    # Skew the input space to determine which simplex cell we're in
    F3 = 1.0/3.0
    # Very nice and simple skew factor for 3D
    s = (x+y+z) * F3
    i = int(x + s)
    j = int(y + s)
    k = int(z + s)

    G3 = 1.0 / 6.0
    t = float(i+j+k) * G3
    # Unskew the cell origin back to (x,y,z) space
    X0 = i - t
    Y0 = j - t
    Z0 = k - t
    # The x,y,z distances from the cell origin
    x0 = x - X0
    y0 = y - Y0
    z0 = z - Z0

    # For the 3D case, the simplex shape is a slightly irregular tetrahedron.
    # Determine which simplex we are in.
    i1, j1, k1 = 0,0,0 # Offsets for second corner of simplex in (i,j,k) coords
    i2, j2, k2 = 0,0,0 # Offsets for third corner of simplex in (i,j,k) coords

    if x0 >= y0:
        if y0 >= z0: # X Y Z order
            i1 = 1
            j1 = 0
            k1 = 0
            i2 = 1
            j2 = 1
            k2 = 0
        elif x0 >= z0: # X Z Y order
            i1 = 1
            j1 = 0
            k1 = 0
            i2 = 1
            j2 = 0
            k2 = 1
        else: # Z X Y order
            i1 = 0
            j1 = 0
            k1 = 1
            i2 = 1
            j2 = 0
            k2 = 1
    else:
        if y0 < z0: # Z Y X order
            i1 = 0
            j1 = 0
            k1 = 1
            i2 = 0
            j2 = 1
            k2 = 1
        elif x0 < z0: # Y Z X order
            i1 = 0
            j1 = 1
            k1 = 0
            i2 = 0
            j2 = 1
            k2 = 1
        else: # Y X Z order
            i1 = 0
            j1 = 1
            k1 = 0
            i2 = 1
            j2 = 1
            k2 = 0

    # A step of (1,0,0) in (i,j,k) means a step of (1-c,-c,-c) in (x,y,z),
    # a step of (0,1,0) in (i,j,k) means a step of (-c,1-c,-c) in (x,y,z), and
    # a step of (0,0,1) in (i,j,k) means a step of (-c,-c,1-c) in (x,y,z), where
    # c = 1/6.
    x1 = x0 - i1 + G3      # Offsets for second corner in (x,y,z) coords
    y1 = y0 - j1 + G3
    z1 = z0 - k1 + G3
    x2 = x0 - i2 + 2.0*G3  # Offsets for third corner in (x,y,z) coords
    y2 = y0 - j2 + 2.0*G3
    z2 = z0 - k2 + 2.0*G3
    x3 = x0 - 1.0 + 3.0*G3 # Offsets for last corner in (x,y,z) coords
    y3 = y0 - 1.0 + 3.0*G3
    z3 = z0 - 1.0 + 3.0*G3

    # Work out the hashed gradient indices of the four simplex corners
    ii = int(i) & 255
    jj = int(j) & 255
    kk = int(k) & 255
    gi0 = _perm[ii+_perm[jj+_perm[kk]]] % 12
    gi1 = _perm[ii+i1+_perm[jj+j1+_perm[kk+k1]]] % 12
    gi2 = _perm[ii+i2+_perm[jj+j2+_perm[kk+k2]]] % 12
    gi3 = _perm[ii+1+_perm[jj+1+_perm[kk+1]]] % 12

    # Calculate the contribution from the four corners
    t0 = 0.6 - x0*x0 - y0*y0 - z0*z0
    t20 = t0 * t0
    t40 = t20 * t20
    if t0 < 0:
        n0 = 0.0
        t0 = 0.0
        t20 = 0.0
        t40 = 0.0
    else:
        n0 = t40 * dot3d(_grad3[gi0], x0, y0, z0)

    t1 = 0.6 - x1*x1 - y1*y1 - z1*z1
    t21 = t1 * t1
    t41 = t21 * t21
    if t1 < 0:
        n1 = 0.0
        t1 = 0.0
        t21 = 0.0
        t41 = 0.0
    else:
        n1 = t41 * dot3d(_grad3[gi1], x1, y1, z1)

    t2 = 0.6 - x2*x2 - y2*y2 - z2*z2
    t22 = t2 * t2
    t42 = t22 * t22
    if t2 < 0:
        n2 = 0.0
        t2 = 0.0
        t22 = 0.0
        t42 = 0.0
    else:
        n2 = t42 * dot3d(_grad3[gi2], x2, y2, z2)

    t3 = 0.6 - x3*x3 - y3*y3 - z3*z3
    t23 = t3 * t3
    t43 = t23 * t23
    if t3 < 0:
        n3 = 0.0
        t3 = 0.0
        t23 = 0.0
        t43 = 0.0
    else:
        n3 = t43 * dot3d(_grad3[gi3], x3, y3, z3)

    # Add contributions from each corner to get the final noise value.
    # The result is scaled to stay just inside [-1,1]
    #noise = 32.0 * (n0 + n1 + n2 + n3)
    noise = 32.0  * (n0 + n1 + n2 + n3)

    temp0 = t20 * t0 * dot3d(_grad3[gi0], x0, y0, z0 )
    dx = temp0 * x0
    dy = temp0 * y0
    dz = temp0 * z0
    
    temp1 = t21 * t1 * dot3d(_grad3[gi1], x1, y1, z1 )
    dx += temp1 * x1
    dy += temp1 * y1
    dz += temp1 * z1
    
    temp2 = t22 * t2 * dot3d(_grad3[gi2], x2, y2, z2 )
    dx += temp2 * x2
    dy += temp2 * y2
    dz += temp2 * z2
    
    temp3 = t23 * t3 * dot3d(_grad3[gi3], x3, y3, z3 )
    dx += temp3 * x3
    dy += temp3 * y3
    dz += temp3 * z3
    dx *= -8.0
    dy *= -8.0
    dz *= -8.0
    #/* This corrects a bug in the original implementation */
    dx += t40 * _grad3[gi0][0] + t41 * _grad3[gi1][0] + t42 * _grad3[gi2][0] + t43 * _grad3[gi3][0]
    dy += t40 * _grad3[gi0][1] + t41 * _grad3[gi1][1] + t42 * _grad3[gi2][1] + t43 * _grad3[gi3][1]
    dz += t40 * _grad3[gi0][2] + t41 * _grad3[gi1][2] + t42 * _grad3[gi2][2] + t43 * _grad3[gi3][2]
    dx *= 16.9446 #/* Scale derivative to match the noise scaling */
    dy *= 16.9446
    dz *= 16.9446
    #print noise, dx, dy, dz
    return noise, [dx, dy, dz]



def dot2d(g, x, y):
    return g[0]*x + g[1]*y

def dot3d(g, x, y, z):
    return g[0]*x + g[1]*y + g[2]*z

def dot4d(g, x, y, z, w):
    return g[0]*x + g[1]*y + g[2]*z + g[3]*w


"""The gradients are the midpoints of the vertices of a cube."""
_grad3 = [
    [1,1,0], [-1,1,0], [1,-1,0], [-1,-1,0],
    [1,0,1], [-1,0,1], [1,0,-1], [-1,0,-1],
    [0,1,1], [0,-1,1], [0,1,-1], [0,-1,-1]
]

"""The gradients are the midpoints of the vertices of a cube."""
_grad4 = [
    [0,1,1,1],  [0,1,1,-1],  [0,1,-1,1],  [0,1,-1,-1],
    [0,-1,1,1], [0,-1,1,-1], [0,-1,-1,1], [0,-1,-1,-1],
    [1,0,1,1],  [1,0,1,-1],  [1,0,-1,1],  [1,0,-1,-1],
    [-1,0,1,1], [-1,0,1,-1], [-1,0,-1,1], [-1,0,-1,-1],
    [1,1,0,1],  [1,1,0,-1],  [1,-1,0,1],  [1,-1,0,-1],
    [-1,1,0,1], [-1,1,0,-1], [-1,-1,0,1], [-1,-1,0,-1],
    [1,1,1,0],  [1,1,-1,0],  [1,-1,1,0],  [1,-1,-1,0],
    [-1,1,1,0], [-1,1,-1,0], [-1,-1,1,0], [-1,-1,-1,0]
]

"""Permutation table.  The same list is repeated twice."""
_perm = [
    151,160,137,91,90,15,131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,
    8,99,37,240,21,10,23,190,6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,
    35,11,32,57,177,33,88,237,149,56,87,174,20,125,136,171,168,68,175,74,165,71,
    134,139,48,27,166,77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,
    55,46,245,40,244,102,143,54,65,25,63,161,1,216,80,73,209,76,132,187,208,89,
    18,169,200,196,135,130,116,188,159,86,164,100,109,198,173,186,3,64,52,217,226,
    250,124,123,5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,
    189,28,42,223,183,170,213,119,248,152,2,44,154,163,70,221,153,101,155,167,43,
    172,9,129,22,39,253,19,98,108,110,79,113,224,232,178,185,112,104,218,246,97,
    228,251,34,242,193,238,210,144,12,191,179,162,241,81,51,145,235,249,14,239,
    107,49,192,214,31,181,199,106,157,184,84,204,176,115,121,50,45,127,4,150,254,
    138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180,

    151,160,137,91,90,15,131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,
    8,99,37,240,21,10,23,190,6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,
    35,11,32,57,177,33,88,237,149,56,87,174,20,125,136,171,168,68,175,74,165,71,
    134,139,48,27,166,77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,
    55,46,245,40,244,102,143,54,65,25,63,161,1,216,80,73,209,76,132,187,208,89,
    18,169,200,196,135,130,116,188,159,86,164,100,109,198,173,186,3,64,52,217,226,
    250,124,123,5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,
    189,28,42,223,183,170,213,119,248,152,2,44,154,163,70,221,153,101,155,167,43,
    172,9,129,22,39,253,19,98,108,110,79,113,224,232,178,185,112,104,218,246,97,
    228,251,34,242,193,238,210,144,12,191,179,162,241,81,51,145,235,249,14,239,
    107,49,192,214,31,181,199,106,157,184,84,204,176,115,121,50,45,127,4,150,254,
    138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180
]

"""A lookup table to traverse the simplex around a given point in 4D."""
_simplex = [
    [0,1,2,3],[0,1,3,2],[0,0,0,0],[0,2,3,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[1,2,3,0],
    [0,2,1,3],[0,0,0,0],[0,3,1,2],[0,3,2,1],[0,0,0,0],[0,0,0,0],[0,0,0,0],[1,3,2,0],
    [0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],
    [1,2,0,3],[0,0,0,0],[1,3,0,2],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,3,0,1],[2,3,1,0],
    [1,0,2,3],[1,0,3,2],[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,0,3,1],[0,0,0,0],[2,1,3,0],
    [0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],
    [2,0,1,3],[0,0,0,0],[0,0,0,0],[0,0,0,0],[3,0,1,2],[3,0,2,1],[0,0,0,0],[3,1,2,0],
    [2,1,0,3],[0,0,0,0],[0,0,0,0],[0,0,0,0],[3,1,0,2],[0,0,0,0],[3,2,0,1],[3,2,1,0]
]
