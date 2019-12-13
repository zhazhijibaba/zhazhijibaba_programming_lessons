from trianglulation import *
from vector import *
import numpy as np
import math
import openmesh as om

theta = np.pi / 6.0
#theta = np.pi / 12.0
# height of coin
a1 = 30
# length of lane
a2 = 180
# width of lane
a3 = 2.2
# thickness of the wall
a4 = 1.2
v1 = a2 * np.cos(theta)
v2 = a1 / np.sin(theta) + v1
v3 = v1 * np.sin(theta)
v4 = v2 * np.sin(theta)
v5 = a1 / np.cos(theta)

mesh = om.TriMesh()
make_block_triangle_mesh(mesh, [0, 0, 0], [v1, 0, 0], [0, 0, v3], [0, a4, 0])
make_block_mesh(mesh, [v1, 0, 0], [-v1, 0, v3], [0, 0, v5], [0, a4, 0])
make_block_triangle_mesh(mesh, [0, a4, 0], [v1, 0, 0], [0, 0, v3], [0, a3, 0])
make_block_triangle_mesh(mesh, [0, a4 + a3, 0], [v1, 0, 0], [0, 0, v3], [0, a4, 0])
make_block_mesh(mesh, [v1, a4 + a3, 0], [-v1, 0, v3], [0, 0, v5], [0, a4, 0])
om.write_mesh("funnel_launcher_test2.obj", mesh)
#om.write_mesh("funnel_launcher_test3.obj", mesh)
