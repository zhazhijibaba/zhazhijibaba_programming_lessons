from vector import *
import openmesh as om
import numpy as np

# create mesh for top part
d1 = np.sqrt(0.5)
mesh = om.TriMesh()
#make_block_mesh(mesh, [0, 0, 2], [5, 0, 0], [0, 5, 0], [0, 0, 1])
make_block_mesh(mesh, [5, 0, 2], [5, 0, 0], [0, 5, 0], [0, 0, 1])
make_block_mesh(mesh, [10, 0, 2], [5, 0, 0], [0, 20, 0], [0, 0, 1])
#make_block_mesh(mesh, [10, 20, 2], [5, 0, 0], [0, 5, 0], [0, 0, 1])
make_block_mesh(mesh, [14.5, 25, 2], [0.5, 0, 0], [0, 0.5, 0], [0, 0, 1])
make_block_mesh(mesh, [10, 25, 2], [4, 0, 0], [0, 0.5, 0], [0, 0, 1])
make_block_mesh(mesh, [15-d1, 0, 2], [0.5*d1, -0.5*d1, 0], [0.5*d1, 0.5*d1, 0], [0, 0, 1])
make_block_mesh(mesh, [15-d1, 0, 2], [-0.5*d1, 0.5*d1, 0], [-0.5*d1, -0.5*d1, 0], [0, 0, 1])
# make hole part
make_pipe_mesh(mesh, [2.5, 2.5, 2], [2.5, 2.5, 3], p2=[1, 1, 0.0], r1=d1, r2=5*d1, n=4)
make_pipe_mesh(mesh, [12.5, 22.5, 2], [12.5, 22.5, 3], p2=[22.5, 12.5, 0.0], r1=d1, r2=5*d1, n=4)


om.write_mesh("rubber_gun_top.obj", mesh)

