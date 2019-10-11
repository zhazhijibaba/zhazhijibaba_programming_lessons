from blocks import *
from vector import *
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import openmesh as om

bb = []
bbd = []
bb_c = []
b1 = Tetrakaidecahedron()
#b1 = Dodecahedron()
bb_c.append(b1.get_centroid())
bb.append(b1)

for i in range(2):
    bb1 = []
    bb_c1 = []
    for b1 in bb:
        # grow tetrakaidecahedron
        cci = b1.get_tetrakaidecahedron_surface_list()
        cc = b1.get_tetrakaidecahedron_surface_coords()
        for ci, c1 in zip(cci, cc):
            n1 = Tetrakaidecahedron()
            if n1.move2surface(ci, c1, bb_c):
                bb1.append(n1)
                bb_c1.append(n1.get_centroid())
            b1.interface_list.append(ci)
        # grow dodecahedron
        cci = b1.get_dodecahedron_surface_list()
        cc = b1.get_dodecahedron_surface_coords()
        for ci, c1 in zip(cci, cc):
            n1 = Dodecahedron()
            if n1.move2surface(c1, bb_c):
                bbd.append(n1)
                bb_c1.append(n1.get_centroid())
            b1.interface_list.append(ci)
    bb = bb + bb1
    bb_c = bb_c + bb_c1

# create mesh for all edges for tetrakaidecahedron
mesh = om.TriMesh()
for b1 in bb:
    v1 = b1.vertex
    for e in b1.edge:
        p0 = v1[e[0]]
        p1 = v1[e[1]]
        make_mesh(mesh, p0, p1, p2=[1.0, 0.0, 0.0], r=0.2, n=6)
# create mesh for all edges for dodecahedron
for b1 in bbd:
    v1 = b1.vertex
    for e in b1.edge:
        p0 = v1[e[0]]
        p1 = v1[e[1]]
        make_mesh(mesh, p0, p1, p2=[1.0, 0.0, 0.0], r=0.4, n=6)
#om.write_mesh("bubble1_dodecahedron.obj", mesh)
om.write_mesh("bubble1.obj", mesh)
