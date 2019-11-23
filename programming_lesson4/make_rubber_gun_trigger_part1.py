from vector import *
import openmesh as om
import numpy as np

# create mesh for bottom part
d1 = np.sqrt(0.5)
mesh = om.TriMesh()
# trigger part
make_block_mesh(mesh, [15-3*d1, -d1, 1], [d1, d1, 0], [-5*d1, 5*d1, 0], [0, 0, 1])
make_block_mesh(mesh, [15-2*d1, 0, 1], [d1, d1, 0], [-6*d1, 6*d1, 0], [0, 0, 1])
make_block_triangle_mesh(mesh, [15-3*d1, 3*d1, 1], [-3, 3, 0], [0, 6, 0], [0, 0, 1])
om.write_mesh("rubber_gun_trigger_part1.obj", mesh)

d2 = 0.25
for i in range(5):
    mesh = om.TriMesh()
    make_block_mesh(mesh, [15-3*d1 + i*d2, -d1 -i*d2, 1], [d1, d1, 0], [-5*d1, 5*d1, 0], [0, 0, 1])
    make_block_mesh(mesh, [15-2*d1 + i*d2, -i*d2, 1], [d1, d1, 0], [-6*d1, 6*d1, 0], [0, 0, 1])
    make_block_triangle_mesh(mesh, [15-3*d1 + i*d2, 3*d1-i*d2, 1], [-3, 3, 0], [0, 6, 0], [0, 0, 1])
    om.write_mesh("rubber_gun_trigger_part1_{0}.obj".format(i), mesh)
