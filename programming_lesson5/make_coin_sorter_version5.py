from vector import *
import openmesh as om
import numpy as np

# version3 slope 15 degree
theta = np.pi / 12.0
# https://en.wikipedia.org/wiki/Coins_of_the_Canadian_dollar
# create mesh for coin sorter
# Nickel 5 cents 21.2mm (1.76mm)
# Dime 10 cents 18.03mm (1.22mm)
# Quatoer 25 cents 23.88mm (1.58mm)
# Loonie $1 26.5mm (1.75mm)
# Toonie $2 28mm (1.8mm)
dd0 = [18.03, 21.2, 23.88, 26.5, 28]
d0 = 0.8
dd = [d + d0 for d in dd0]
d1 = 35
d2 = 2
# slope 30 degree
d3 = d1 / np.cos(theta)

mesh = om.TriMesh()
# part 1 sorter
x0 = 0
# screen layer
for i in range(len(dd)):
    ri = dd[i] / 2
    make_block_mesh(mesh, [x0, 0, 0], [d3 - dd[i], 0, 0], [0, d1, 0], [0, 0, d2])
    x0 = x0 + d3 - dd[i]
    make_pipe_square_mesh(mesh, [x0 + ri, ri, 0], [x0 + ri, ri, d2], p2=[x0 + ri, 0.0, 0.0], r1=ri, r2=ri, n=256)
    make_block_mesh(mesh, [x0, dd[i], 0], [dd[i], 0, 0], [0, d1 - dd[i], 0], [0, 0, d2])
    x0 = x0 + dd[i]
make_block_mesh(mesh, [x0, 0, 0], [d2, 0, 0], [0, d1, 0], [0, 0, d2])
x0 = x0 + d2
# wall block
# total length of sortor
d4 = x0
make_block_mesh(mesh, [0, 0, 0], [0, -d2, 0], [d4, 0, 0], [0, 0, 8*d2])
om.write_mesh("coin_sorter_v5_p1.obj", mesh)

# part 2 holder
mesh = om.TriMesh()
d5 = d4 * np.cos(theta)
d6 = d2 * np.cos(theta)
d7 = 40 + 2*d2
d8 = 1.0
x1 = 0
make_block_mesh(mesh, [0, 0, 0], [d5, 0, 0], [0, d1, 0], [0, 0, d2])
make_block_mesh(mesh, [x1, 0, 0], [d6, 0, 0], [0, d1, 0], [0, 0, d7 + d4 * np.sin(theta)])
make_block_mesh(mesh, [x1, 0, 0], [d6 + 2*d2, 0, 0], [0, d8, 0], [0, 0, d7 + d4 * np.sin(theta) + 6*d2])
make_block_triangle_mesh(mesh, [x1, 0, d7 + d4 * np.sin(theta)], [0, d1, d1*np.tan(theta)], [0, d1, 0], [d6, 0, 0])
x1 = x1 + d6
for i in range(len(dd)):
    x1 = x1 + d1
    dh = d7 + (d4 - (i + 1) * d3) * np.sin(theta)
    make_block_mesh(mesh, [x1, 0, 0], [d8, 0, 0], [0, d1, 0], [0, 0, dh])
    make_block_triangle_mesh(mesh, [x1, 0, dh], [0, d1, d1*np.tan(theta)], [0, d1, 0], [d8, 0, 0])
    if i < len(dd) - 1:
        make_block_mesh(mesh, [x1, 0, 0], [d8 + 2*d2, 0, 0], [0, d8, 0], [0, 0, dh + 6*d2])
    else:
        make_block_mesh(mesh, [x1, 0, 0], [d8 + d8, 0, 0], [0, d8, 0], [0, 0, dh + 6*d2])
        make_block_mesh(mesh, [x1 + d8, 0, 0], [d8, 0, 0], [0, d1, 0], [0, 0, dh + 6*d2])
        make_block_triangle_mesh(mesh, [x1 + d8, 0, dh + 6*d2], [0, d1, d1*np.tan(theta)], [0, d1, 0], [d8, 0, 0])

om.write_mesh("coin_sorter_v5_p2.obj", mesh)

# part 2 coin collector
mesh = om.TriMesh()
d9 = d1 - d8
d10 = d9 - 2*d8
d11 = d7 - 2*d2
make_rod_mesh(mesh, [0, 0, 0], [0, 0, d8], p2=[1.0, 0.0, 0.0], r=d9 / 2.0, n=256)
make_pipe_mesh(mesh, [0,0,d8], [0,0,d11], p2=[1.0, 0.0, 0.0], r1=d10/2.0, r2=d9/2.0, n=256)
om.write_mesh("coin_sorter_v5_p3.obj", mesh)
