import numpy as np
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from rmsd import *

Dodecahedron_points=[
 3.14980,   0      ,   6.29961,
-3.14980,   0      ,   6.29961,
 4.19974,   4.19974,   4.19974,
 0      ,   6.29961,   3.14980,
-4.19974,   4.19974,   4.19974,
-4.19974,  -4.19974,   4.19974,
 0      ,  -6.29961,   3.14980,
 4.19974,  -4.19974,   4.19974,
 6.29961,   3.14980,   0      ,
-6.29961,   3.14980,   0      ,
-6.29961,  -3.14980,   0      ,
 6.29961,  -3.14980,   0      ,
 4.19974,   4.19974,  -4.19974,
 0      ,   6.29961,  -3.14980,
-4.19974,   4.19974,  -4.19974,
-4.19974,  -4.19974,  -4.19974,
 0      ,  -6.29961,  -3.14980,
 4.19974,  -4.19974,  -4.19974,
 3.14980,   0      ,  -6.29961,
-3.14980,   0      ,  -6.29961]

class Dodecahedron(object):
    def __init__(self):
        self.vertex = np.array(Dodecahedron_points).reshape((20, 3))
        # face with anti-clockwise vertex order
        self.face = [
                [0, 2, 3, 4, 1],
                [5, 1, 4, 9, 10],
                [0, 1, 5, 6, 7],
                [2, 0, 7, 11, 8],
                [3, 2, 8, 12, 13],
                [4, 3, 13, 14, 9],
                [17, 16, 15, 19, 18],
                [6, 5, 10, 15, 16],
                [15, 10, 9, 14, 19],
                [14, 13, 12, 18, 19],
                [16, 17, 11, 7, 6],
                [18, 12, 8, 11, 17]]
        self.edge = self.make_edge_list()
        self.interface_list = []

    def make_edge_list(self):
        edge_list = []
        for f1 in self.face:
            for i in range(len(f1)):
                v1 = f1[i - 1]
                v2 = f1[i]
                v12 = [v1, v2]
                if v1 > v2:
                    v12 = [v2, v1]
                if v12 not in edge_list:
                    edge_list.append(v12)
        return edge_list

    def show_block(self):
        v1 = self.vertex
        mpl.rcParams['legend.fontsize'] = 10
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.scatter(v1[:,0], v1[:,1], v1[:,2], label='parametric curve')
        i = 0
        for p1 in v1:
            ax.text(p1[0], p1[1], p1[2], "{0}".format(i))
            i += 1
        for e in self.edge:
            ax.plot([v1[e[0]][0], v1[e[1]][0]],
                [v1[e[0]][1], v1[e[1]][1]],
                [v1[e[0]][2], v1[e[1]][2]])
        plt.show()

    def get_interface(self):
        return  [self.face[i] for i in self.interface_list]

    def get_surface(self):
        return [self.face[i] for i in (set(range(len(self.face))) - set(self.interface_list))]

    def get_centroid(self):
        return centroid(self.vertex)

    def in_centroid_list(self, c1, cc):
        for cc1 in cc:
            d2 = (c1[0] - cc1[0])**2 + (c1[1] - cc1[1])**2 + (c1[2] - cc1[2])**2
            if d2 < 0.00000001:
                return True
        return False

    # move block to position defined by surface vertex coords of vv
    def move2surface(self, vv, bb_c=[]):
        vv_back = np.array(vv).copy()
        for s1 in self.face:
            for i in range(len(s1)):
                svv = np.array([self.vertex[s1[i - j]] for j in range(len(s1))]).copy()
                # get centroids
                c_vv = centroid(vv_back)
                c_svv = centroid(svv)
                # move to centroids
                vv0 = vv_back - c_vv
                svv0 = svv - c_svv
                U = kabsch(svv0, vv0)
                svv0 = np.dot(svv0, U)
                rmsd_value = rmsd(svv0, vv0)
                # find the matched surface
                if rmsd_value < 0.00001:
                    # perform superposition for whole block
                    self.vertex -= c_svv
                    self.vertex = np.dot(self.vertex, U)
                    self.vertex += c_vv
                    c_new = self.get_centroid()
                    if self.in_centroid_list(c_new, bb_c):
                        continue
                    return True
        return False


Tetrakaidecahedron_points=[
 3.14980,   3.70039,   5,
-3.14980,   3.70039,   5,
-5      ,   0      ,   5,
-3.14980,  -3.70039,   5,
 3.14980,  -3.70039,   5,
 5      ,   0      ,   5,
 4.19974,   5.80026,   0.80026,
-4.19974,   5.80026,   0.80026,
-6.85020,   0      ,   1.29961,
-4.19974,  -5.80026,   0.80026,
 4.19974,  -5.80026,   0.80026,
 6.85020,   0      ,   1.29961,
 5.80026,   4.19974,  -0.80026,
 0      ,   6.85020,  -1.29961,
-5.80026,   4.19974,  -0.80026,
-5.80026,  -4.19974,  -0.80026,
 0      ,  -6.85020,  -1.29961,
 5.80026,  -4.19974,  -0.80026,
 3.70039,   3.14980,  -5, 
 0      ,   5      ,  -5,
-3.70039,   3.14980,  -5,
-3.70039,  -3.14980,  -5,
 0      ,  -5      ,  -5,
 3.70039,  -3.14980,  -5]


class Tetrakaidecahedron(object):
    def __init__(self):
        self.vertex = np.array(Tetrakaidecahedron_points).reshape((24, 3))
        # face with anti-clockwise vertex order
        self.face = [
                [0,1,2,3,4,5],
                [18,19,20,21,22,23],
                [0,6,13,7,1],
                [1,7,14,8,2],
                [2,8,15,9,3],
                [3,9,16,10,4],
                [4,10,17,11,5],
                [5,11,12,6,0],
                [18,19,13,6,12],
                [19,20,14,7,13],
                [20,21,15,8,14],
                [21,22,16,9,15],
                [22,23,17,10,16],
                [23,18,12,11,17]]
        self.edge = self.make_edge_list()
        self.interface_list = []
        self.tetrakaidecahedron_surface_list = [0, 1, 3, 4, 6, 7, 8, 9, 11, 12]
        self.dodecahedron_surface_list = [2, 5, 10, 13]

    def make_edge_list(self):
        edge_list = []
        for f1 in self.face:
            for i in range(len(f1)):
                v1 = f1[i - 1]
                v2 = f1[i]
                v12 = [v1, v2]
                if v1 > v2:
                    v12 = [v2, v1]
                if v12 not in edge_list:
                    edge_list.append(v12)
        return edge_list

    def show_block(self):
        v1 = self.vertex
        mpl.rcParams['legend.fontsize'] = 10
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.scatter(v1[:,0], v1[:,1], v1[:,2], label='parametric curve')
        i = 0
        for p1 in v1:
            ax.text(p1[0], p1[1], p1[2], "{0}".format(i))
            i += 1
        for e in self.edge:
            ax.plot([v1[e[0]][0], v1[e[1]][0]],
                [v1[e[0]][1], v1[e[1]][1]],
                [v1[e[0]][2], v1[e[1]][2]])
        plt.show()

    def get_interface(self):
        return  [self.face[i] for i in self.interface_list]

    def get_surface(self):
        return [self.face[i] for i in (set(range(len(self.face))) - set(self.interface_list))]

    def get_tetrakaidecahedron_surface(self):
        return [self.face[i] for i in (set(self.tetrakaidecahedron_surface_list) - set(self.interface_list))]

    def get_tetrakaidecahedron_surface_list(self, si=-1):
        if si < 0:
            return list(set(self.tetrakaidecahedron_surface_list) - set(self.interface_list))
        else:
            # get list of surface with same type
            tt = [[0, 1], [3, 6, 9, 12], [4, 7, 8, 11]]
            for t1 in tt:
                if si in t1:
                    return list(set(t1) - set(self.interface_list))
            

    def get_tetrakaidecahedron_surface_coords(self):
        ss = self.get_tetrakaidecahedron_surface()
        cc = []
        for s1 in ss:
            c1 = []
            for v1 in s1:
               c1.append(self.vertex[v1])
            cc.append(c1)
        return cc

    def get_dodecahedron_surface(self):
        return [self.face[i] for i in (set(self.dodecahedron_surface_list) - set(self.interface_list))]

    def get_dodecahedron_surface_list(self):
        return list(set(self.dodecahedron_surface_list) - set(self.interface_list))
            

    def get_dodecahedron_surface_coords(self):
        ss = self.get_dodecahedron_surface()
        cc = []
        for s1 in ss:
            c1 = []
            for v1 in s1:
               c1.append(self.vertex[v1])
            cc.append(c1)
        return cc

    def get_centroid(self):
        return centroid(self.vertex)

    def in_centroid_list(self, c1, cc):
        for cc1 in cc:
            d2 = (c1[0] - cc1[0])**2 + (c1[1] - cc1[1])**2 + (c1[2] - cc1[2])**2
            if d2 < 0.00000001:
                return True
        return False

    # move block to position defined by surface vertex coords of vv
    def move2surface(self, vi, vv, bb_c=[]):
        vv_back = np.array(vv).copy()
        ss_list = self.get_tetrakaidecahedron_surface_list(vi)
        for si in ss_list:
            s1 = self.face[si]
            if len(s1) == len(vv):
                for i in range(len(s1)):
                    svv = np.array([self.vertex[s1[i - j]] for j in range(len(s1))]).copy()
                    # get centroids
                    c_vv = centroid(vv_back)
                    c_svv = centroid(svv)
                    # move to centroids
                    vv0 = vv_back - c_vv
                    svv0 = svv - c_svv
                    U = kabsch(svv0, vv0)
                    svv0 = np.dot(svv0, U)
                    rmsd_value = rmsd(svv0, vv0)
                    # find the matched surface
                    if rmsd_value < 0.00001:
                        # perform superposition for whole block
                        self.vertex -= c_svv
                        self.vertex = np.dot(self.vertex, U)
                        self.vertex += c_vv
                        c_new = self.get_centroid()
                        self.interface_list.append(si)
                        if self.in_centroid_list(c_new, bb_c):
                            continue
                        return True
        return False

def are_points_same_face(pp, face):
    for f1 in face:
        if all(p1 in f1 for p1 in pp):
            return True
    return False

