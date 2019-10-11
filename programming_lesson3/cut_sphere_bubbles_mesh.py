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
initial_pose(b1, [0.87, 1.3, 1.7, 2.0*np.pi/7, np.pi/7, np.pi/3])
#initial_pose(b1, [0, 0, 0, 0, 0, 0])
bb_c.append(b1.get_centroid())
bb.append(b1)

for i in range(4):
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
frame_r = 1.5
# sphere radius
sphere_r = 35
sphere_r2 = sphere_r * sphere_r
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
        # check if the sphere cuttting the sphere surface
        d0 = p0[0]**2 + p0[1]**2 + p0[2]**2
        d1 = p1[0]**2 + p1[1]**2 + p1[2]**2
        if (d0 < sphere_r2 and d1 > sphere_r2) or (d0 > sphere_r2 and d1 < sphere_r2):
            # if p0 is outside the sphere, switch p0 and p1
            # so that p0 should be inside the sphere
            if d0 > sphere_r2 and d1 < sphere_r2:
                p0 = v1[e[1]]
                p1 = v1[e[0]]
                pv = -pv
            # find the cutting point
            # the line x = x0 + dx*t, y = y0 + dy*t, z = z0 + dz*t
            # where dx, dy, dz is defined by pv
            # if the sphere is intersected with line, then
            # (x0 + dx*t)**2 + (y0 + dy*t)**2 + (z0 + dz*t)**2 = sphere_r2
            # solve equation for t with a = dx**2 + dy**2 + dz**2
            # b = 2*(x0*dx + y0*dy + z0*dz), c = x0**2 + y0**2 + z0**2 - sphere_r2
            # t = (-b + sqrt(b**2 - 4ac))/(2a) for p0 inside and p1 outside, t should be positive
            a = pv[0]**2 + pv[1]**2 + pv[2]**2
            b = 2 * (p0[0]*pv[0] + p0[1]*pv[1] + p0[2]*pv[2])
            c = p0[0]**2 + p0[1]**2 + p0[2]**2 - sphere_r2
            t = (-b + sqrt(b**2 - 4 * a * c)) / 2 / a
            cut_p = p0 + t * pv
            # add the cutting point the cutting point lest
            cut_pp.append([cut_p, e[0], e[1]])

    # make mesh if the two cutting point is in the same block surface
    for i in range(len(cut_pp)):
        for j in range(i + 1, len(cut_pp)):
            b1 = cut_pp[i]
            b2 = cut_pp[j]
            # b1 and b2 are in same block surface
            if are_points_same_face([b1[1], b1[2], b2[1], b2[2]], f1):
                #print b1[0], b2[0]
                p0 = b1[0]
                p1 = b2[0]
                make_mesh(mesh, p0, p1, p2=[1.0, 1.0, 1.0], r=frame_r, n=6)

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
om.write_mesh("bubble_sphere_cut2.obj", mesh)
