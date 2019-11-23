from vector import *
import openmesh as om
import numpy as np

# create mesh for bottom part
d1 = np.sqrt(0.5)
mesh = om.TriMesh()
make_block_mesh(mesh, [0, 0, 0], [10, 0, 0], [0, 5, 0], [0, 0, 1])
make_block_mesh(mesh, [10, 0, 0], [5, 0, 0], [0, 25, 0], [0, 0, 1])
make_block_mesh(mesh, [14.5, 25, 0], [0.5, 0, 0], [0, 0.5, 0], [0, 0, 1])
make_block_mesh(mesh, [10, 25, 0], [4, 0, 0], [0, 0.5, 0], [0, 0, 1])
make_block_mesh(mesh, [15-d1, 0, 0], [0.5*d1, -0.5*d1, 0], [0.5*d1, 0.5*d1, 0], [0, 0, 1])
make_block_mesh(mesh, [15-d1, 0, 0], [-0.5*d1, 0.5*d1, 0], [-0.5*d1, -0.5*d1, 0], [0, 0, 1])
# middle part
make_block_mesh(mesh, [15-6.1*d1, -0.1*d1, 1], [d1, d1, 0], [-5*d1, 5*d1, 0], [0, 0, 1])
make_block_mesh(mesh, [15-8.1*d1, 3.9*d1, 1], [d1, d1, 0], [-2*d1, 2*d1, 0], [0, 0, 1])
make_block_mesh(mesh, [0, 0, 1], [5, 0, 0], [0, 5, 0], [0, 0, 1])
make_block_mesh(mesh, [10, 15, 1], [5, 0, 0], [0, 10, 0], [0, 0, 1])
make_block_mesh(mesh, [15-d1, d1, 1], [d1, 0, 0], [0, 15-d1, 0], [0, 0, 1])
make_block_mesh(mesh, [10, 5*d1+6, 1], [d1, 0, 0], [0, 15-5*d1-6, 0], [0, 0, 1])
make_block_triangle_mesh(mesh, [15-d1, d1, 1], [-0.2, 0.2, 0], [0, 0.4, 0], [0, 0, 1])
# top part
make_block_mesh(mesh, [2, 2, 2], [0.9, 0, 0], [0, 0.9, 0], [0, 0, 1])
make_block_mesh(mesh, [12, 22, 2], [0.9, 0, 0], [0, 0.9, 0], [0, 0, 1])

# trigger part1
#make_block_mesh(mesh, [15-3*d1, -d1, 1], [d1, d1, 0], [-5*d1, 5*d1, 0], [0, 0, 1])
#make_block_mesh(mesh, [15-2*d1, 0, 1], [d1, d1, 0], [-6*d1, 6*d1, 0], [0, 0, 1])
#make_block_triangle_mesh(mesh, [15-3*d1, 3*d1, 1], [-3, 3, 0], [0, 6, 0], [0, 0, 1])

# trigger part2
#make_block_triangle_mesh(mesh, [10+d1, 5*d1+6, 1], [5-2*d1, 0, 0], [0, -5+2*d1, 0], [0, 0, 1])
#make_block_mesh(mesh, [10+d1, 15, 1], [0, -15+5*d1+6, 0], [5-2*d1, 0, 0], [0, 0, 1])
#make_block_mesh(mesh, [10+d1, 5*d1+6, 1], [-5, 0, 0], [0, -1.5, 0], [0, 0, 1])

om.write_mesh("rubber_gun_bottom.obj", mesh)

