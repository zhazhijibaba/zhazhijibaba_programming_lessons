from trianglulation import *
from vector import *
import numpy as np
import math
import openmesh as om

mesh = om.TriMesh()
#make_pipe_mesh(mesh, [0,0,150], [0,0,155], r1=55, r2=60, n=100)
make_pipe_mesh(mesh, [0,0,62], [0,0,70], p2=[1.0, 0.0, 0.0], r1=73, r2=81, n=100)
make_rod_mesh(mesh, [77,0,-100], [77,0,70-1], p2=[1.0, 0.0, 0.0], r=4, n=32)
make_rod_mesh(mesh, [0,77,-100], [0,77,70-1], p2=[1.0, 0.0, 0.0], r=4, n=32)
make_rod_mesh(mesh, [-77,0,-100], [-77,0,70-1], p2=[1.0, 0.0, 0.0], r=4, n=32)
make_rod_mesh(mesh, [0,-77,-100], [0,-77,70-1], p2=[1.0, 0.0, 0.0], r=4, n=32)
om.write_mesh("funnel_stand_test1.obj", mesh)
