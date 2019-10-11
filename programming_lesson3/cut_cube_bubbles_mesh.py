from blocks import *
from vector import *
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import openmesh as om
import numpy as np

bb = []
bbd = []
bb_c = []
b1 = Tetrakaidecahedron()
# pose vector 6: translation x, y, z, rotation about x, y, z axis
initial_pose(b1, [0, 0, 0, 2.0*np.pi/7, np.pi/7, np.pi/3])
#initial_pose(b1, [0, 0, 0, 0, 0, 0])
bb_c.append(b1.get_centroid())
bb.append(b1)

for i in range(5):
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

mesh = om.TriMesh()
frame_r = 1.0
# box: xmin, xmax, ymin, ymax, zmin, zmax
box = [-30, 30, -30, 30, -15, 15]
# make 6 plaens, xmin, xmax, ymin, ymax, zmin, zmax
planes = [
        [box[0], 0, 0, 1, 0, 0],
        [box[1], 0, 0, -1, 0, 0],
        [0, box[2], 0, 0, 1, 0],
        [0, box[3], 0, 0, -1, 0],
        [0, 0, box[4], 0, 0, 1],
        [0, 0, box[5], 0, 0, -1]]
# create mesh for all cutting edges
for b1 in bb + bbd:
    v1 = b1.vertex
    f1 = b1.face
    ## find all cutting points
    cut_pp = []
    for e in b1.edge:
        p0 = v1[e[0]]
        p1 = v1[e[1]]
        pv = np.array([p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]])
        for ai, a1 in enumerate(planes):
            a0 = np.array(a1[:3])
            av = np.array(a1[3:])
            av = av / np.linalg.norm(av)
            pav = np.dot(pv, av)
            # line is parallel to the plane
            if abs(pav) < 0.000001:
                continue
            # check cutting edge
            d = np.dot((a0 - p0), av) / pav
            # if the intersection point is in the line
            if d >= 0 and d <= 1:
                cut_p = p0 + d * pv
                cut_pp.append([cut_p, e[0], e[1], ai])

    # make mesh if the two cutting point is in the same surface
    for i in range(len(cut_pp)):
        for j in range(i + 1, len(cut_pp)):
            b1 = cut_pp[i]
            b2 = cut_pp[j]
            # b1 and b2 are not in same plane
            if b1[3] != b2[3]:
                continue
            # b1 and b2 are in same surface
            if are_points_same_face([b1[1], b1[2], b2[1], b2[2]], f1):
                #print b1[0], b2[0]
                p0 = b1[0]
                p1 = b2[0]
                pv = np.array([p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]])
                # move the outside point on border
                # planes xmin, xmax
                if b1[3] == 0 or b1[3] == 1:
                    p0[1] = box[2] if p0[1] < box[2] else p0[1]
                    p0[1] = box[3] if p0[1] > box[3] else p0[1]
                    p0[2] = box[4] if p0[2] < box[4] else p0[2]
                    p0[2] = box[5] if p0[2] > box[5] else p0[2]
                    p1[1] = box[2] if p1[1] < box[2] else p1[1]
                    p1[1] = box[3] if p1[1] > box[3] else p1[1]
                    p1[2] = box[4] if p1[2] < box[4] else p1[2]
                    p1[2] = box[5] if p1[2] > box[5] else p1[2]
                # planes ymin, ymax
                if b1[3] == 2 or b1[3] == 3:
                    p0[0] = box[0] if p0[0] < box[0] else p0[0]
                    p0[0] = box[1] if p0[0] > box[1] else p0[0]
                    p0[2] = box[4] if p0[2] < box[4] else p0[2]
                    p0[2] = box[5] if p0[2] > box[5] else p0[2]
                    p1[0] = box[0] if p1[0] < box[0] else p1[0]
                    p1[0] = box[1] if p1[0] > box[1] else p1[0]
                    p1[2] = box[4] if p1[2] < box[4] else p1[2]
                    p1[2] = box[5] if p1[2] > box[5] else p1[2]
                # planes zmin, zmax
                if b1[3] == 4 or b1[3] == 5:
                    p0[0] = box[0] if p0[0] < box[0] else p0[0]
                    p0[0] = box[1] if p0[0] > box[1] else p0[0]
                    p0[1] = box[2] if p0[1] < box[2] else p0[1]
                    p0[1] = box[3] if p0[1] > box[3] else p0[1]
                    p1[0] = box[0] if p1[0] < box[0] else p1[0]
                    p1[0] = box[1] if p1[0] > box[1] else p1[0]
                    p1[1] = box[2] if p1[1] < box[2] else p1[1]
                    p1[1] = box[3] if p1[1] > box[3] else p1[1]
                make_mesh(mesh, p0, p1, p2=[1.0, 1.0, 1.0], r=frame_r, n=6)

# make box frame
make_mesh(mesh, [box[0], box[2], box[4]], [box[0], box[2], box[5]], p2=[1.0, 1.0, 1.0], r=frame_r, n=6)
make_mesh(mesh, [box[0], box[3], box[4]], [box[0], box[3], box[5]], p2=[1.0, 1.0, 1.0], r=frame_r, n=6)
make_mesh(mesh, [box[0], box[2], box[4]], [box[0], box[3], box[4]], p2=[1.0, 1.0, 1.0], r=frame_r, n=6)
make_mesh(mesh, [box[0], box[2], box[5]], [box[0], box[3], box[5]], p2=[1.0, 1.0, 1.0], r=frame_r, n=6)
make_mesh(mesh, [box[1], box[2], box[4]], [box[1], box[2], box[5]], p2=[1.0, 1.0, 1.0], r=frame_r, n=6)
make_mesh(mesh, [box[1], box[3], box[4]], [box[1], box[3], box[5]], p2=[1.0, 1.0, 1.0], r=frame_r, n=6)
make_mesh(mesh, [box[1], box[2], box[4]], [box[1], box[3], box[4]], p2=[1.0, 1.0, 1.0], r=frame_r, n=6)
make_mesh(mesh, [box[1], box[2], box[5]], [box[1], box[3], box[5]], p2=[1.0, 1.0, 1.0], r=frame_r, n=6)
make_mesh(mesh, [box[0], box[2], box[4]], [box[1], box[2], box[4]], p2=[1.0, 1.0, 1.0], r=frame_r, n=6)
make_mesh(mesh, [box[0], box[2], box[5]], [box[1], box[2], box[5]], p2=[1.0, 1.0, 1.0], r=frame_r, n=6)
make_mesh(mesh, [box[0], box[3], box[4]], [box[1], box[3], box[4]], p2=[1.0, 1.0, 1.0], r=frame_r, n=6)
make_mesh(mesh, [box[0], box[3], box[5]], [box[1], box[3], box[5]], p2=[1.0, 1.0, 1.0], r=frame_r, n=6)

if False:
    # create mesh for all edges for tetrakaidecahedron and dodecahedron
    for b1 in bb + bbd:
        v1 = b1.vertex
        for e in b1.edge:
            p0 = v1[e[0]]
            p1 = v1[e[1]]
            # move the outside point on border
            # planes xmin, xmax
            if p0[0] < box[0] and p1[0] < box[0]:
                continue
            if p0[1] < box[2] and p1[1] < box[2]:
                continue
            if p0[2] < box[4] and p1[2] < box[4]:
                continue
            if p0[0] > box[1] and p1[0] > box[1]:
                continue
            if p0[1] > box[3] and p1[1] > box[3]:
                continue
            if p0[2] > box[5] and p1[2] > box[5]:
                continue
            # both inside
            if p0[0] > box[0] and p0[0] < box[1] and p0[1] > box[2] and p0[1] < box[3] and p0[2] > box[4] and p0[2] < box[5]:
                if p1[0] > box[0] and p1[0] < box[1] and p1[1] > box[2] and p1[1] < box[3] and p1[2] > box[4] and p1[2] < box[5]:
                    make_mesh(mesh, p0, p1, p2=[1.0, 0.1, 1.0], r=frame_r*0.5, n=6)
                    continue
            if False:
                p0[0] = box[0] if p0[0] < box[0] else p0[0]
                p0[0] = box[1] if p0[0] > box[1] else p0[0]
                p0[1] = box[2] if p0[1] < box[2] else p0[1]
                p0[1] = box[3] if p0[1] > box[3] else p0[1]
                p0[2] = box[4] if p0[2] < box[4] else p0[2]
                p0[2] = box[5] if p0[2] > box[5] else p0[2]
                p1[0] = box[0] if p1[0] < box[0] else p1[0]
                p1[0] = box[1] if p1[0] > box[1] else p1[0]
                p1[1] = box[2] if p1[1] < box[2] else p1[1]
                p1[1] = box[3] if p1[1] > box[3] else p1[1]
                p1[2] = box[4] if p1[2] < box[4] else p1[2]
                p1[2] = box[5] if p1[2] > box[5] else p1[2]
                make_mesh(mesh, p0, p1, p2=[1.0, 0.1, 1.0], r=frame_r*0.5, n=6)

# output final buble box
om.write_mesh("bubble_cut3.obj", mesh)
