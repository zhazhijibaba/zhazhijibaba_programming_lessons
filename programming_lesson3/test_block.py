from blocks import *

#b1 = Dodecahedron()
b1 = Tetrakaidecahedron()
v1 = b1.vertex

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.scatter(v1[:,0], v1[:,1], v1[:,2], label='parametric curve')
i = 0
for p1 in v1:
    ax.text(p1[0], p1[1], p1[2], "{0}".format(i))
    i += 1
print len(b1.edge)
print b1.edge
for e in b1.edge:
    ax.plot([v1[e[0]][0], v1[e[1]][0]],
        [v1[e[0]][1], v1[e[1]][1]],
        [v1[e[0]][2], v1[e[1]][2]])
ax.legend()

plt.show()
