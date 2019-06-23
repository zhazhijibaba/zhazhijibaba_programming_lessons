import numpy as np
import openmesh as om
from math import cos, sin, sqrt
import argparse

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--debug", required=False, help="debug mode", action="store_true")
ap.add_argument("-f", "--leaf", required=False, help="build leaf", action="store_true")
ap.add_argument("-r", "--leafr", required=False, help="leaf sphere radius", default=10.0, type=float)
ap.add_argument("-l", "--level", required=False, help="total level of tree", default=5, type=int)
ap.add_argument("-w", "--width", required=False, help="trunk width", default=10, type=float)
ap.add_argument("-n", "--length", required=False, help="trunk length", default=30, type=float)
ap.add_argument("-i", "--rwidth", required=False, help="trunk width ratio", default=0.7, type=float)
ap.add_argument("-p", "--rlength", required=False, help="trunk length ration", default=0.7, type=float)
ap.add_argument("-t", "--delta", required=False, help="angle between two branches", default=30, type=float)
ap.add_argument("-e", "--theta1", required=False, help="angle of branch #1", default=30, type=float)
ap.add_argument("-a", "--theta2", required=False, help="angle of branch #2", default=30, type=float)
ap.add_argument("-o", "--output", required=False, help="output file name .obj", default="output", type=str)
args = vars(ap.parse_args())

# generate icosphere leaf
def generate_icosphere(mesh, radius, center):

    r = (1.0 + np.sqrt(5.0)) / 2.0
    vertices = np.array([
        [-1.0,   r, 0.0],
        [ 1.0,   r, 0.0],
        [-1.0,  -r, 0.0],
        [ 1.0,  -r, 0.0],
        [0.0, -1.0,   r],
        [0.0,  1.0,   r],
        [0.0, -1.0,  -r],
        [0.0,  1.0,  -r],
        [  r, 0.0, -1.0],
        [  r, 0.0,  1.0],
        [ -r, 0.0, -1.0],
        [ -r, 0.0,  1.0],
        ], dtype=float)

    length = np.linalg.norm(vertices, axis=1).reshape((-1, 1))
    vertices = vertices / length * radius + center
    
    vv = []
    for v in vertices:
        vv.append(mesh.add_vertex(v))

    faces = np.array([
        [0, 11, 5],
        [0, 5, 1],
        [0, 1, 7],
        [0, 7, 10],
        [0, 10, 11],
        [1, 5, 9],
        [5, 11, 4],
        [11, 10, 2],
        [10, 7, 6],
        [7, 1, 8],
        [3, 9, 4],
        [3, 4, 2],
        [3, 2, 6],
        [3, 6, 8],
        [3, 8, 9],
        [5, 4, 9],
        [2, 4, 11],
        [6, 2, 10],
        [8, 6, 7],
        [9, 8, 1],
        ])

    for f in faces:
        fh0 = mesh.add_face(vv[f[0]], vv[f[1]], vv[f[2]])

# vector perpendicular to plane of p0->p1 and p1->p2
# returns the projection of p1->p3 to the plane perpendicular to p1->p2
def make_perpendicular_unit_vector(p0, p1, p3, p2):
    v1 = np.array([p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]])
    v2 = np.array([p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]])
    v3 = np.cross(v1, v2)
    v4 = np.array([p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]])
    v5 = np.cross(v4, v2)
    v2_u = v2 / np.linalg.norm(v2)
    v4_u = v4 / np.linalg.norm(v4)
    angle = np.arccos(np.clip(np.dot(v2_u, v4_u), -1.0, 1.0))
    delta = np.pi / 2 - angle
    rmat = rotation_matrix(v5, delta)
    v6 = np.dot(rmat, np.array(v4).T).T
    return v6 / np.linalg.norm(v6)

def rotation_matrix(axis, theta):
    mat = np.eye(3,3)
    axis = axis/sqrt(np.dot(axis, axis))
    a = cos(theta/2.)
    b, c, d = -axis*sin(theta/2.)

    return np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
                  [2*(b*c+a*d), a*a+c*c-b*b-d*d, 2*(c*d-a*b)],
                  [2*(b*d-a*c), 2*(c*d+a*b), a*a+d*d-b*b-c*c]])


# tree node
class Node:

    def __init__(self, data):
        # edges direction check list
        self.edges = []

        self.left = None
        self.right = None
        self.data = data

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def insert_left(self, data):
        if self.left is None:
            self.left = Node(data)

    def insert_right(self, data):
        if self.right is None:
            self.right = Node(data)

    def mesh(self, mesh, base):
        if len(self.edges) == 0:
            self.edges.append([base[1], base[2]])
            self.edges.append([base[2], base[3]])
            self.edges.append([base[3], base[1]])
        v1 = mesh.add_vertex(mesh.point(base[1]))
        v2 = mesh.add_vertex(mesh.point(base[2]))
        v3 = mesh.add_vertex(mesh.point(base[3]))
        #pp1 = [mesh.point(self.data[2]), mesh.point(self.data[3]), mesh.point(self.data[4])]
        #pp2 = [mesh.point(base[2]), mesh.point(base[3]), mesh.point(base[4])]
        pp1 = [self.data[1], self.data[2], self.data[3]]
        #pp2 = [base[2], base[3], base[4]]
        pp2 = [v1, v2, v3]
        # find minimum distance pairs
        ff = self.find_min_pairs(mesh, pp1, pp2)
        #ff = []
        #for i in [2, 3, 4]:
        #    ii = self.find_closest_point(mesh.point(self.data[i]), pp)
        #    ff.append([self.data[i], base[2 + ii]])
        # add triangle faces
        #print ff[0][1], ff[1][1], ff[0][0]
        mesh.add_face(self.correct_edges(ff[0][1], ff[1][1], ff[0][0]))
        mesh.add_face(self.correct_edges(ff[1][1], ff[2][1], ff[1][0]))
        mesh.add_face(self.correct_edges(ff[2][1], ff[0][1], ff[2][0]))
        mesh.add_face(self.correct_edges(ff[2][0], ff[1][0], ff[2][1]))
        mesh.add_face(self.correct_edges(ff[1][0], ff[0][0], ff[1][1]))
        mesh.add_face(self.correct_edges(ff[0][0], ff[2][0], ff[0][1]))
        if self.left:
            self.left.mesh(mesh, self.data)
        if self.right:
            self.right.mesh(mesh, self.data)

    def correct_edges(self, e1, e2, e3):
        if [e1, e2] in self.edges or [e2, e3] in self.edges or [e3, e1] in self.edges:
            self.edges.append([e3, e2])
            self.edges.append([e2, e1])
            self.edges.append([e1, e3])
            #print [e3, e2, e1]
            return [e3, e2, e1]
        else:
            self.edges.append([e1, e2])
            self.edges.append([e2, e3])
            self.edges.append([e3, e1])
            #print [e1, e2, e3]
            return [e1, e2, e3]

    def find_closest_point(self, p, pp):
        dd = [((p[0] - p1[0]) ** 2 + (p[1] - p1[1]) ** 2 + (p[2] - p1[2]) ** 2) for p1 in pp]
        return np.argmin(dd)

    def build_branch(self, level, mesh, base, s_length, r, s_thickness, theta1, theta2, delta, leaf=False, leaf_r=0.0):
        a0 = np.array(base)
        a1 = np.array(self.data[0])
        a2 = mesh.point(self.data[1])
        a01 = a1 - a0
        r = r * s_thickness
        zx = np.array([0, 0, 1])
        axis1 = np.cross(a01, zx)
        axis2 = np.cross(axis1, a01)
        # make left branch
        rmat = rotation_matrix(axis2, theta1)
        a12 = np.dot(rmat, a01.T).T * s_length
        p0 = a1 + a12
        u0 = make_perpendicular_unit_vector(a0, a1, a2, p0) * r
        #rmat = rotation_matrix(a12, np.pi / 6)
        #u0 = np.dot(rmat, np.array(u0).T).T
        p1 = np.array(p0) + u0 
        rmat = rotation_matrix(a12, np.pi * 2 / 3)
        u1 = np.dot(rmat, np.array(u0).T).T
        p2 = u1 + p0
        u2 = np.dot(rmat, np.array(u1).T).T
        p3 = u2 + p0
        v1 = mesh.add_vertex(p1)
        v2 = mesh.add_vertex(p2)
        v3 = mesh.add_vertex(p3)
        data2 = [p0, v1, v2, v3]
        self.insert_left(data2)

        # make right branch
        rmat = rotation_matrix(axis2, -theta2)
        a12 = np.dot(rmat, a01.T).T * s_length
        rmat = rotation_matrix(a01, delta)
        a12 = np.dot(rmat, a12.T).T
        p0 = a1 + a12
        u0 = make_perpendicular_unit_vector(a0, a1, a2, p0) * r
        #rmat = rotation_matrix(a12, np.pi / 6)
        #u0 = np.dot(rmat, np.array(u0).T).T
        p1 = np.array(p0) + u0 
        rmat = rotation_matrix(a12, np.pi * 2 / 3)
        u1 = np.dot(rmat, np.array(u0).T).T
        p2 = u1 + p0
        u2 = np.dot(rmat, np.array(u1).T).T
        p3 = u2 + p0
        v1 = mesh.add_vertex(p1)
        v2 = mesh.add_vertex(p2)
        v3 = mesh.add_vertex(p3)
        data2 = [p0, v1, v2, v3]
        self.insert_right(data2)

        level = level - 1
        if level < 1:
            if leaf:
                #print "make leaf", level
                generate_icosphere(mesh, leaf_r, self.left.data[0])
                generate_icosphere(mesh, leaf_r, self.right.data[0])
            return
        self.left.build_branch(level, mesh, self.data[0], s_length, r, s_thickness, theta1, theta2, delta, leaf=leaf, leaf_r=leaf_r)
        self.right.build_branch(level, mesh, self.data[0], s_length, r, s_thickness, theta1, theta2, delta, leaf=leaf, leaf_r=leaf_r)

    def find_min_pairs(self, mesh, pp1, pp2):
        import itertools
        ppp = [zip(x, range(len(pp2))) for x in itertools.permutations(range(len(pp1)),len(pp2))]
        dd = []
        for pp in ppp:
            d1 = 0
            for p1 in pp:
                i = p1[0]
                j = p1[1]
                x1 = mesh.point(pp1[i])
                x2 = mesh.point(pp2[j])
                d1 += np.sqrt((x1[0] - x2[0]) ** 2 + (x1[1] - x2[1]) ** 2 + (x1[2] - x2[2]) ** 2)
            dd.append(d1)
        i = np.argmin(dd)
        return [[pp1[i1], pp2[i2]] for i1, i2 in ppp[i]]

# virtual 2-branch tree model
class Tree2:

    def __init__(self, levels, thickness, length, scaling_length, scaling_thickness, theta1, theta2, delta, leaf=False, leaf_r=0.0):
        self.levels = levels
        self.thickness = thickness
        self.length = length
        self.base = None
        self.s_length = scaling_length
        self.s_thickness = scaling_thickness
        self.theta1 = theta1
        self.theta2 = theta2
        self.delta = delta
        self.node = None
        self.leaf = leaf
        self.leaf_r = leaf_r

        self.mesh = om.TriMesh()
        self.build_root()
        self.build_branches()

    def build_root(self):
        # make base
        r = self.thickness
        v1 = self.mesh.add_vertex([0, r, 0])
        v2 = self.mesh.add_vertex([0.5 * np.sqrt(3) * r, -0.5 * r, 0])
        v3 = self.mesh.add_vertex([-0.5 * np.sqrt(3) * r, -0.5 * r, 0])
        self.base = [[0, 0, 0], v1, v2, v3]
        # make root trunk
        r = self.thickness * self.s_thickness
        h = self.length
        v1 = self.mesh.add_vertex([0, r, h])
        v2 = self.mesh.add_vertex([0.5 * np.sqrt(3) * r, -0.5 * r, h])
        v3 = self.mesh.add_vertex([-0.5 * np.sqrt(3) * r, -0.5 * r, h])
        data = [[0, 0, h], v1, v2, v3]
        self.node = Node(data)

    def build_branches(self):
        theta1 = self.theta1
        theta2 = self.theta2
        delta = self.delta
        d = self.length * self.s_length
        r = self.thickness * self.s_thickness * self.s_thickness
        h = self.length
        data1 = self.node.data
        # initial left branch position
        p0 = np.array([d * np.sin(theta1), 0, h + d * np.cos(theta1)])
        u0 = make_perpendicular_unit_vector(self.base[0], data1[0], self.mesh.point(data1[1]), p0) * r
        #rmat = rotation_matrix(p0 - np.array(data1[0]), np.pi / 6)
        #u0 = np.dot(rmat, np.array(u0).T).T
        p1 = np.array(p0) + u0 
        rmat = rotation_matrix(p0 - np.array(data1[0]), np.pi * 2 / 3)
        u1 = np.dot(rmat, np.array(u0).T).T
        p2 = u1 + p0
        u2 = np.dot(rmat, np.array(u1).T).T
        p3 = u2 + p0
        v1 = self.mesh.add_vertex(p1)
        v2 = self.mesh.add_vertex(p2)
        v3 = self.mesh.add_vertex(p3)
        data2 = [p0, v1, v2, v3]
        self.node.insert_left(data2)
        #v0 = self.mesh.add_vertex(p0)
        #self.node.get_left().build_branch(self.levels - 1, self.mesh, self.base[0], self.s_length, r, self.s_thickness, theta1, theta2, delta)
        self.node.get_left().build_branch(self.levels - 1, self.mesh, self.node.data[0], self.s_length, r, self.s_thickness, theta1, theta2, delta, leaf=self.leaf, leaf_r=self.leaf_r)

        # initial right brach position
        p0 = [-d * np.sin(theta2), 0, h + d * np.cos(theta2)]
        #v1 = self.mesh.add_vertex(p0)
        #v2 = self.mesh.add_vertex([0, 0, 0])
        #self.mesh.add_face(v2, v1, v0)
        rmat = rotation_matrix(np.array([0, 0, 1]), delta)
        p0 = np.dot(rmat, np.array(p0).T).T
        u0 = make_perpendicular_unit_vector(self.base[0], data1[0], self.mesh.point(data1[1]), p0) * r
        #rmat = rotation_matrix(p0 - np.array(data1[0]), np.pi / 6)
        #u0 = np.dot(rmat, np.array(u0).T).T
        p1 = np.array(p0) + u0 
        rmat = rotation_matrix(p0 - np.array(data1[0]), np.pi * 2 / 3)
        u1 = np.dot(rmat, np.array(u0).T).T
        p2 = u1 + p0
        u2 = np.dot(rmat, np.array(u1).T).T
        p3 = u2 + p0
        v1 = self.mesh.add_vertex(p1)
        v2 = self.mesh.add_vertex(p2)
        v3 = self.mesh.add_vertex(p3)
        data2 = [p0, v1, v2, v3]
        self.node.insert_right(data2)
        #v1 = self.mesh.add_vertex(p1)
        #self.mesh.add_face(v0, v1, v2)
        #self.node.get_right().build_branch(self.levels - 1, self.mesh, self.base[0], self.s_length, r, self.s_thickness, theta1, theta2, delta)
        self.node.get_right().build_branch(self.levels - 1, self.mesh, self.node.data[0], self.s_length, r, self.s_thickness, theta1, theta2, delta, leaf=self.leaf, leaf_r=self.leaf_r)

    def build_mesh(self):
        self.mesh.add_face(self.base[1], self.base[2], self.base[3])
        self.node.mesh(self.mesh, self.base)

def main():
    theta1 = np.pi / 180 * args["theta1"]
    theta2 = np.pi / 180 * args["theta2"]
    delta = np.pi / 180 * args["delta"]
    trunk_thickness = args["width"]
    trunk_length = args["length"]
    ratio_thickness = args["rwidth"]
    ratio_length = args["rlength"]

    # make tree
    tree = Tree2(args["level"], trunk_thickness, trunk_length, ratio_length, ratio_thickness, theta1, theta2, delta, leaf=args["leaf"], leaf_r=args["leafr"])
    # build mesh
    tree.build_mesh()
    # output mesh file
    om.write_mesh(args["output"] + ".obj", tree.mesh)

if __name__ == "__main__":
    main()
