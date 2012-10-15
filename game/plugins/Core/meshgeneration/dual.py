import numpy as np
import math

import meshutil


class DualContour:
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
        self.vindex = {}

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
            [ k for (k,v) in enumerate(self.cube_verts) if v[i] == a and v[j] == b ]
            for a in range(2)
            for b in range(2)
            for i in range(3) 
            for j in range(3) if i != j ]

    def estimate_hermite(self, v0, v1):
        den, der = raw_noise_3d(v0[0]/15.0, v0[1]/15.0, v0[2]/15.0)
        den2, der2 = raw_noise_3d(v1[0]/15.0, v1[1]/15.0, v1[2]/15.0)
        den = (den + 1) / 2
        den2 = (den2 + 1) / 2
        t0 = (den + den2) / 2
        x0 = (1.-t0)*v0 + t0*v1
        tempder = der + der2
        dfx0 = [0,0,0]
        #fix scaling for this just like the density
        dfx0[0], dfx0[1], dfx0[2] = tempder[0] / 2, tempder[1] / 2, tempder[2] / 2
        return (x0, dfx0)

    def generateMesh(self):
        dc_verts = []
        for x in xrange(0, self.size - 1):
            for y in xrange(0, self.size - 1):
                for z in xrange(0, self.size - 1):
                    o = np.array([x, y, z])
                    #Get signs for cube
                    cube_signs = []
                    """for v in self.cube_verts:
                        cv = o+v
                        if self.blocks[cv[0]][cv[1]][cv[2]] > 0:
                            cube_signs.append(True)
                        else:
                            cube_signs.append(False)
                    print cube_signs"""
                    """cube_signs = [ self.blocks[o+v][][]>0 for v in self.cube_verts ]
                    cube_signs = [True, True, True, True, True, True, True, True]
                    cube_signs = [False, False, False, False, False, False, False, False]"""

                    h_data = []
                    #for e in self.cube_edges:
                    #    if cube_signs[e[0]] != cube_signs[e[1]]:
                    #        h_data.append(self.estimate_hermite(o+self.cube_verts[e[0]], o+self.cube_verts[e[1]]))
                    for e in self.cube_edges:
                        h_data.append(self.estimate_hermite(o+self.cube_verts[e[0]], o+self.cube_verts[e[1]]))

                    #print h_data

                    #Solve qef to get vertex
                    A = [n for p, n in h_data]
                    b = [np.dot(p, n) for p, n in h_data]
                    v, residue, rank, s = la.lstsq(A, b)

                    #Throw out failed solutions
                    if la.norm(v - o) > 2:
                        continue

                    #Emit one vertex per every cube that crosses
                    self.vindex[tuple(o)] = len(dc_verts)
                    #print self.vindex
                    dc_verts.append(v)
                    #print dc_verts

        #Construct faces
        dc_faces = []
        for x, y, z in it.product(range(self.size - 1), range(self.size - 1), range(self.size - 1)):
            if not (x, y, z) in self.vindex:
                continue

            #Emit one face per each edge that crosses
            o = np.array([x, y, z])
            for i in range(3):
                for j in range(i):
                    if tuple(o + self.dirs[i]) in self.vindex and tuple(o + self.dirs[j]) in self.vindex and tuple(o + self.dirs[i] + self.dirs[j]) in self.vindex:
                        dc_faces.append( [self.vindex[tuple(o)], self.vindex[tuple(o+self.dirs[i])], self.vindex[tuple(o+self.dirs[j])]] )
                        dc_faces.append( [self.vindex[tuple(o+self.dirs[i]+self.dirs[j])], self.vindex[tuple(o+self.dirs[j])], self.vindex[tuple(o+self.dirs[i])]] )


        dc_triangles = []
        for face in dc_faces:
            v1 = dc_verts[face[0]]
            v2 = dc_verts[face[1]]
            v3 = dc_verts[face[2]]
            dc_triangles.append(((v1[0], v1[1], v1[2]),
                (v2[0], v2[1], v2[2]),
                (v3[0], v3[1], v3[2])))
        return dc_triangles
