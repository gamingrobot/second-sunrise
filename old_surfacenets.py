class SurfaceNet:
    def __init__(self, chunk, size, chunks, pradius, noise):
        #Random test comment
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

        self.dirs = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.R = [1, (16 + 1), (16 + 1) * (16 + 1)]
        self.cube_edges = [
            0, 1,  # First 3 edges are used for generating faces
            0, 2,
            0, 4,
            1, 3,  # Order for these edges does not matter
            1, 5,
            2, 3,
            2, 6,
            3, 7,
            4, 5,
            4, 6,
            5, 7,
            6, 7]

    def generateMesh(self):
        vertices = []
        faces = []
        vindex = {}
        buf_no = 1
        for x in xrange(0, self.size - 1):
            buf_no ^= 1
            self.R[2] = -self.R[2]
            m = 1 + (16 + 1) * (1 + buf_no * (16 + 1))
            for y in xrange(0, self.size - 1):
                m += 2
                for z in xrange(0, self.size - 1):
                    m += 1
                    pv = []
                    #note try and do this without flipped
                    pv.append(self.blocks[x, y, z].getDensity())
                    pv.append(self.blocks[x + 1, y, z].getDensity())
                    pv.append(self.blocks[x, y + 1, z].getDensity())  # flipped
                    pv.append(self.blocks[x + 1, y + 1, z].getDensity())  # flipped
                    pv.append(self.blocks[x, y, z + 1].getDensity())
                    pv.append(self.blocks[x + 1, y, z + 1].getDensity())
                    pv.append(self.blocks[x, y + 1, z + 1].getDensity())  # flipped
                    pv.append(self.blocks[x + 1, y + 1, z + 1].getDensity())  # flipped
                    g = 0
                    mask = 0
                    for p in pv:
                        if p < self.level:
                            mask |= 1 << g
                        else:
                            mask |= 0
                        g += 1
                    #check edgemask
                    edge_mask = edgeTable[mask]
                    if not edge_mask:
                        continue
                    #sum up intersections
                    v = [0.0, 0.0, 0.0]
                    e_count = 0
                    for i in xrange(0, 12):
                        if not (edge_mask & (1 << i)):
                            continue
                        e_count += 1
                        e0 = self.cube_edges[i << 1]
                        e1 = self.cube_edges[(i << 1) + 1]
                        g0 = pv[e0]
                        g1 = pv[e1]
                        t = g0 - g1
                        if math.fabs(t) > 0.000001:
                            t = g0 / t
                        else:
                            continue
                        k = 1
                        for j in xrange(0, 3):
                            a = e0 & k
                            if a & (~e1):
                                if a:  # was !!a
                                    v[j] += 1.0 - t
                                else:
                                    v[j] += t
                            else:
                                if a:  # was !!a
                                    v[j] += 1.0
                                else:
                                    v[j] += 0
                            k <<= 1

                    #adverage edge intersections to get vertex
                    s = 1.0 / e_count
                    v[0] = x + s * v[0]
                    v[1] = y + s * v[1]
                    v[2] = z + s * v[2]
                    vindex[m] = len(vertices)
                    vertices.append(v)

                    for i in xrange(0, 3):
                        if not (edge_mask & (1 << i)):
                            continue
                        iu = (i + 1) % 3
                        iv = (i + 2) % 3
                        cord = [x, y, z]
                        if cord[iu] == 0 or cord[iv] == 0:
                            continue

                        du = self.R[iu]
                        dv = self.R[iv]
                        if(mask & 1):
                            faces.append([vindex[m], vindex[m - du], vindex[m - du - dv], vindex[m - dv]])
                        else:
                            faces.append([vindex[m], vindex[m - dv], vindex[m - du - dv], vindex[m - du]])
        print faces
        return self.triangles


"""class SurfaceNet:
    def __init__(self, chunk, size, chunks, pradius, noise):
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

        self.center = np.array([16, 16, 16])
        self.radius = 5

        #Cardinal directions
        self.dirs = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

        #Vertices of cube
        self.cube_verts = [np.array([x, y, z])
            for x in range(2)
            for y in range(2)
            for z in range(2)]

        #Edges of cube
        self.cube_edges = [
            [k for (k, v) in enumerate(self.cube_verts) if v[i] == a and v[j] == b]
            for a in range(2)
            for b in range(2)
            for i in range(3)
            for j in range(3) if i != j]

    def generateMesh(self):
        triangles = self.dual_contour(self.test_f, self.test_df, 25)
        #print triangles
        return triangles

    #Use non-linear root finding to compute intersection point
    def estimate_hermite(self, f, df, v0, v1):
        t0 = opt.brentq(lambda t: f((1. - t) * v0 + t * v1), 0, 1)
        x0 = (1. - t0) * v0 + t0 * v1
        return (x0, df(x0))

    #Input:
    # f = implicit function
    # df = gradient of f
    # nc = resolution
    def dual_contour(self, f, df, nc):
        #Compute vertices
        dc_verts = []
        vindex = {}
        for x, y, z in it.product(range(nc), range(nc), range(nc)):
            pv = []
            #note try and do this without flipped
            pv.append(self.blocks[x, y, z].getDensity())
            pv.append(self.blocks[x + 1, y, z].getDensity())
            pv.append(self.blocks[x, y + 1, z].getDensity())  # flipped
            pv.append(self.blocks[x + 1, y + 1, z].getDensity())  # flipped
            pv.append(self.blocks[x, y, z + 1].getDensity())
            pv.append(self.blocks[x + 1, y, z + 1].getDensity())
            pv.append(self.blocks[x, y + 1, z + 1].getDensity())  # flipped
            pv.append(self.blocks[x + 1, y + 1, z + 1].getDensity())  # flipped
            g = 0
            mask = 0
            for p in pv:
                if p < self.level:
                    mask |= 1 << g
                else:
                    mask |= 0
                g += 1
            o = np.array([x, y, z])

            #Get signs for cube
            cube_signs = [f(o + v) > 0 for v in self.cube_verts]

            if all(cube_signs) or not any(cube_signs):
                continue

            #Estimate hermite data
            h_data = [self.estimate_hermite(f, df, o + self.cube_verts[e[0]], o + self.cube_verts[e[1]])
                for e in self.cube_edges if cube_signs[e[0]] != cube_signs[e[1]]]

            #Solve qef to get vertex
            A = [n for p, n in h_data]
            b = [np.dot(p, n) for p, n in h_data]
            v, residue, rank, s = la.lstsq(A, b)

            #Throw out failed solutions
            if la.norm(v - o) > 2:
                continue

            #Emit one vertex per every cube that crosses
            vindex[tuple(o)] = len(dc_verts)
            dc_verts.append(v)

        #Construct faces
        dc_faces = []
        for x, y, z in it.product(range(nc), range(nc), range(nc)):
            if not (x, y, z) in vindex:
                continue

            #Emit one face per each edge that crosses
            o = np.array([x, y, z])
            for i in range(3):
                for j in range(i):
                    if mask & 1:
                        dc_faces.append((vindex[tuple(o)], vindex[tuple(o + self.dirs[i])], vindex[tuple(o + self.dirs[j])]))
                        dc_faces.append((vindex[tuple(o + self.dirs[i] + self.dirs[j])], vindex[tuple(o + self.dirs[j])], vindex[tuple(o + self.dirs[i])]))
                    else:
                        dc_faces.append((vindex[tuple(o + self.dirs[j])], vindex[tuple(o + self.dirs[i])], vindex[tuple(o)]))
                        dc_faces.append((vindex[tuple(o + self.dirs[i])], vindex[tuple(o + self.dirs[j])], vindex[tuple(o + self.dirs[i] + self.dirs[j])]))
                    #if tuple(o + self.dirs[i]) in vindex and tuple(o + self.dirs[j]) in vindex and tuple(o + self.dirs[i] + self.dirs[j]) in vindex:
                        #dc_faces.append((vindex[tuple(o)], vindex[tuple(o + self.dirs[i])], vindex[tuple(o + self.dirs[j])]))
                        #dc_faces.append((vindex[tuple(o + self.dirs[i] + self.dirs[j])], vindex[tuple(o + self.dirs[j])], vindex[tuple(o + self.dirs[i])]))
                        #v0_1 = vindex[tuple(o)]
                        #v0_2 = vindex[tuple(o + self.dirs[i] + self.dirs[j])]
                        #v1 = vindex[tuple(o + self.dirs[j])]
                        #v2 = vindex[tuple(o + self.dirs[i])]
                        #if i == 1 and j == 0:
                        #    dc_faces.append((v0_1, v2, v1))
                        #    dc_faces.append((v0_2, v1, v2))
                        #elif i == 2 and j == 0:
                        #    dc_faces.append((v0_2, v2, v1))
                        #    dc_faces.append((v0_1, v1, v2))
                        #elif i == 2 and j == 1:
                        #    dc_faces.append((v0_2, v1, v2))
                        #    dc_faces.append((v0_1, v2, v1))

        dc_triangles = []
        for face in dc_faces:
            v1 = dc_verts[face[0]]
            v2 = dc_verts[face[1]]
            v3 = dc_verts[face[2]]
            dc_triangles.append(((v1[0], v1[1], v1[2]),
                (v2[0], v2[1], v2[2]),
                (v3[0], v3[1], v3[2])))
        return dc_triangles

    def test_f(self, x):
        d = x - self.center
        return np.dot(d, d) - self.radius ** 2

    def test_df(self, x):
        d = x - self.center
        return d / math.sqrt(np.dot(d, d))"""