from trianglulation import *
from vector import *
import numpy as np
import math
import openmesh as om

mesh = om.TriMesh()
make_funnel_mesh(mesh, [0,0,0], [0,0,3.8], p2=[1.0, 0.0, 0.0], z0=-0.5, c1=1.0, r1=15.0, r2=0.1, n=100, m=50)
om.write_mesh("funnel_test1.obj", mesh)
