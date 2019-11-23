from vector import *
import openmesh as om
import numpy as np

# create mesh for bottom part
d1 = np.sqrt(0.5)
mesh = om.TriMesh()
# trigger part
make_block_triangle_mesh(mesh, [10+d1, 5*d1+6, 1], [5-2*d1, 0, 0], [0, -5+2*d1, 0], [0, 0, 1])
make_block_mesh(mesh, [10+d1, 15, 1], [0, -15+5*d1+6, 0], [5-2*d1, 0, 0], [0, 0, 1])
make_block_mesh(mesh, [10+d1, 5*d1+6, 1], [-5, 0, 0], [0, -1.5, 0], [0, 0, 1])
om.write_mesh("rubber_gun_trigger_part2.obj", mesh)

d2 = 0.5
for i in range(5):
    mesh = om.TriMesh()
    make_block_triangle_mesh(mesh, [10+d1, 5*d1+6 - i*d2, 1], [5-2*d1, 0, 0], [0, -5+2*d1, 0], [0, 0, 1])
    make_block_mesh(mesh, [10+d1, 15 - i*d2, 1], [0, -15+5*d1+6, 0], [5-2*d1, 0, 0], [0, 0, 1])
    make_block_mesh(mesh, [10+d1, 5*d1+6 - i*d2, 1], [-5, 0, 0], [0, -1.5, 0], [0, 0, 1])
    om.write_mesh("rubber_gun_trigger_part2_{0}.obj".format(i), mesh)
