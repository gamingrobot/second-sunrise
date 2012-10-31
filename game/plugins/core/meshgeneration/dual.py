import numpy as np
import numpy.linalg as la
import scipy.optimize as opt
import itertools
import math


class DualContour:
    def __init__(self):
        self.isovalue = 0.0

        self.center = np.array([8, 8, 8])
        self.radius = 4

        #Cardinal directions
        self.dirs = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

        #Vertices of cube
        """self.cube_verts = [np.array([x, y, z])
            for x in range(2)
            for y in range(2)
            for z in range(2)]"""
        self.cube_verts = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]

        #Edges of cube
        """self.cube_edges = [ 
            [k for (k, v) in enumerate(self.cube_verts) if v[i] == a and v[j] == b]
            for a in range(2)
            for b in range(2)
            for i in range(3)
            for j in range(3) if i != j]"""

        self.cube_edges = [[0, 1], [0, 2], [0, 1], [0, 4], [0, 2], [0, 4], [2, 3], [1, 3], [4, 5], [1, 5], [4, 6], [2, 6], [4, 5], [4, 6], [2, 3], [2, 6], [1, 3], [1, 5], [6, 7], [5, 7], [6, 7], [3, 7], [5, 7], [3, 7]]

        self.center = np.array([16, 16, 16])
        self.radius = 10

    def estimate_hermite(self, f, df, v0, v1):
        t0 = opt.brentq(lambda t: f((1. - t) * v0 + t * v1), 0, 1)
        x0 = (1. - t0) * v0 + t0 * v1
        return (x0, df(x0))

    def generateMesh(self, terrain, size, lod):
        dc_verts = []
        vindex = {}
        done = False
        #for x, y, z in itertools.product(xrange(0, size - 1), xrange(0, size - 1), xrange(0, size - 1)):
        while not done:
            x, y, z = 13, 9, 9
            o = np.array([x, y, z])
            #Get signs for cube
            #cube_signs = [self.f(o + v) > 0 for v in self.cube_verts]
            cube_signs = []
            for v in self.cube_verts:
                #calculate the output given a xyz
                sign = self.f(o + v)
                if sign > self.isovalue:
                    cube_signs.append(True)
                else:
                    cube_signs.append(False)

            print cube_signs

            #if all are True or all are False skip this run of the loop, there is no sign change
            if all(cube_signs) or not any(cube_signs):
                continue

            #Estimate hermite data
            #h_data = [self.estimate_hermite(self.f, self.df, o+self.cube_verts[e[0]], o+self.cube_verts[e[1]]) 
            #    for e in self.cube_edges if cube_signs[e[0]] != cube_signs[e[1]]]
            h_data = []
            for e in self.cube_edges:
                if cube_signs[e[0]] != cube_signs[e[1]]:
                    #input f, df, and 2 verts out comes p and n
                    h_data.append(self.estimate_hermite(self.f, self.df, o + self.cube_verts[e[0]], o + self.cube_verts[e[1]]))

            #Solve qef to get vertex
            #A = [n for p, n in h_data]
            #b = [np.dot(p, n) for p, n in h_data]
            #v, residue, rank, s = la.lstsq(A, b)
            A = []
            b = []
            for p, n in h_data:
                print p, n
                A.append(n)
                b.append(np.dot(p, n))
            v, residue, rank, s = la.lstsq(A, b)

            #Throw out failed solutions
            print v
            #print la.norm(v - o)
            if la.norm(v - o) > 2:
                continue

            #Emit one vertex per every cube that crosses
            vindex[tuple(o)] = len(dc_verts)
            dc_verts.append(v)
            done = True

        """#Construct faces
        dc_faces = []
        for x, y, z in itertools.product(xrange(0, size - 1), xrange(0, size - 1), xrange(0, size - 1)):
            if not (x, y, z) in vindex:
                continue

            #Emit one face per each edge that crosses
            o = np.array([x, y, z])
            for i in range(3):
                for j in range(i):
                    if tuple(o + self.dirs[i]) in vindex and tuple(o + self.dirs[j]) in vindex and tuple(o + self.dirs[i] + self.dirs[j]) in vindex:
                        dc_faces.append( [vindex[tuple(o)], vindex[tuple(o+self.dirs[i])], vindex[tuple(o+self.dirs[j])]] )
                        dc_faces.append( [vindex[tuple(o+self.dirs[i]+self.dirs[j])], vindex[tuple(o+self.dirs[j])], vindex[tuple(o+self.dirs[i])]] )

        dc_triangles = []
        for face in dc_faces:
            v1 = dc_verts[face[0]]
            v2 = dc_verts[face[1]]
            v3 = dc_verts[face[2]]
            dc_triangles.append(((v1[0], v1[1], v1[2]),
                (v2[0], v2[1], v2[2]),
                (v3[0], v3[1], v3[2])))
        return dc_triangles"""
        return []


    def f(self, x):
        d = x-self.center
        return np.dot(d,d) - self.radius**2

    def df(self, x):
        d = x-self.center
        return d / math.sqrt(np.dot(d,d))



    """def estimate_hermite(self, v0, v1):
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
        return (x0, dfx0)"""


    def generateMesh_old(self, terrain, size, lod):
        dc_verts = []
        for x, y, z in itertools.product(xrange(0, size - 1), xrange(0, size - 1), xrange(0, size - 1)):
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
