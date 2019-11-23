import numpy as np
from math import cos, sin, sqrt

# generate a block based on v1=p0->p1, v2=p0->p2, v3=p0->p3
# p4=p0+v1+v2, p5=p0+v2+v3, p6=p0+v3+v1, p7=p0+v1+v2+v3
def make_block_mesh(mesh, p0, v1, v2, v3):
    p1 = np.array([v1[0] + p0[0], v1[1] + p0[1], v1[2] + p0[2]])
    p2 = np.array([v2[0] + p0[0], v2[1] + p0[1], v2[2] + p0[2]])
    p3 = np.array([v3[0] + p0[0], v3[1] + p0[1], v3[2] + p0[2]])
    p4 = np.array([v1[0] + p2[0], v1[1] + p2[1], v1[2] + p2[2]])
    p5 = np.array([v2[0] + p3[0], v2[1] + p3[1], v2[2] + p3[2]])
    p6 = np.array([v3[0] + p1[0], v3[1] + p1[1], v3[2] + p1[2]])
    p7 = np.array([v3[0] + p4[0], v3[1] + p4[1], v3[2] + p4[2]])
    # add vertex
    a0 = mesh.add_vertex(p0)
    a1 = mesh.add_vertex(p1)
    a2 = mesh.add_vertex(p2)
    a3 = mesh.add_vertex(p3)
    a4 = mesh.add_vertex(p4)
    a5 = mesh.add_vertex(p5)
    a6 = mesh.add_vertex(p6)
    a7 = mesh.add_vertex(p7)
    # make face
    mesh.add_face(a4, a0, a2)
    mesh.add_face(a0, a4, a1)
    mesh.add_face(a3, a2, a0)
    mesh.add_face(a2, a3, a5)
    mesh.add_face(a5, a4, a2)
    mesh.add_face(a4, a5, a7)
    mesh.add_face(a7, a1, a4)
    mesh.add_face(a1, a7, a6)
    mesh.add_face(a6, a0, a1)
    mesh.add_face(a0, a6, a3)
    mesh.add_face(a6, a5, a3)
    mesh.add_face(a5, a6, a7)

# generate a block based on v1=p0->p1, v2=p0->p2, v3=p0->p3
# p4=p3+v1, p5=p3+v2
def make_block_triangle_mesh(mesh, p0, v1, v2, v3):
    p1 = np.array([v1[0] + p0[0], v1[1] + p0[1], v1[2] + p0[2]])
    p2 = np.array([v2[0] + p0[0], v2[1] + p0[1], v2[2] + p0[2]])
    p3 = np.array([v3[0] + p0[0], v3[1] + p0[1], v3[2] + p0[2]])
    p4 = np.array([v1[0] + p3[0], v1[1] + p3[1], v1[2] + p3[2]])
    p5 = np.array([v2[0] + p3[0], v2[1] + p3[1], v2[2] + p3[2]])
    # add vertex
    a0 = mesh.add_vertex(p0)
    a1 = mesh.add_vertex(p1)
    a2 = mesh.add_vertex(p2)
    a3 = mesh.add_vertex(p3)
    a4 = mesh.add_vertex(p4)
    a5 = mesh.add_vertex(p5)
    # make face
    mesh.add_face(a0, a1, a2)
    mesh.add_face(a3, a1, a0)
    mesh.add_face(a1, a3, a4)
    mesh.add_face(a4, a2, a1)
    mesh.add_face(a2, a4, a5)
    mesh.add_face(a5, a0, a2)
    mesh.add_face(a0, a5, a3)
    mesh.add_face(a3, a5, a4)

# generate mesh based on p0->p1
def make_rod_mesh(mesh, p0, p1, p2=[1.0, 0.0, 0.0], r=1.0, n=3):
    p0 = np.array(p0)
    p1 = np.array(p1)
    v1 = np.array([p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]])
    v2 = np.array([p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]])
    v3 = np.cross(v1, v2)
    if np.linalg.norm(v3) == 0:
        return
    v3_u = v3 / np.linalg.norm(v3)
    delta = 2.0 * np.pi / n
    rmat = rotation_matrix(v1, delta)
    o1 = mesh.add_vertex(p0)
    o2 = mesh.add_vertex(p1)
    aa = []
    bb = []
    for i in range(n):
        v3_u = np.dot(rmat, np.array(v3_u).T).T
        aa.append(mesh.add_vertex(p0 + v3_u * r))
        bb.append(mesh.add_vertex(p1 + v3_u * r))

    for i in range(n):
        a1 = aa[i - 1]
        a2 = aa[i]
        b1 = bb[i - 1]
        b2 = bb[i]
        mesh.add_face(o1, a1, a2)
        mesh.add_face(o2, b2, b1)
        mesh.add_face(a2, a1, b1)
        mesh.add_face(b2, a2, b1)

def make_pipe_mesh(mesh, p0, p1, p2=[1.0, 0.0, 0.0], r1=1.0, r2=2.0, n=3):
    if r1 > r2:
        rt = r1
        r1 = r2
        r2 = rt
    p0 = np.array(p0)
    p1 = np.array(p1)
    v1 = np.array([p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]])
    v2 = np.array([p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]])
    v3 = np.cross(v1, v2)
    if np.linalg.norm(v3) == 0:
        return
    v3_u = v3 / np.linalg.norm(v3)
    delta = 2.0 * np.pi / n
    rmat = rotation_matrix(v1, delta)
    o1 = mesh.add_vertex(p0)
    o2 = mesh.add_vertex(p1)
    aa1 = []
    aa2 = []
    bb1 = []
    bb2 = []
    for i in range(n):
        v3_u = np.dot(rmat, np.array(v3_u).T).T
        aa1.append(mesh.add_vertex(p0 + v3_u * r1))
        aa2.append(mesh.add_vertex(p0 + v3_u * r2))
        bb1.append(mesh.add_vertex(p1 + v3_u * r1))
        bb2.append(mesh.add_vertex(p1 + v3_u * r2))

    for i in range(n):
        a11 = aa1[i - 1]
        a12 = aa1[i]
        a21 = aa2[i - 1]
        a22 = aa2[i]
        b11 = bb1[i - 1]
        b12 = bb1[i]
        b21 = bb2[i - 1]
        b22 = bb2[i]
        mesh.add_face(a11, a21, a12)
        mesh.add_face(a12, a21, a22)
        mesh.add_face(a21, b21, a22)
        mesh.add_face(a22, b21, b22)
        mesh.add_face(b22, b21, b11)
        mesh.add_face(b22, b11, b12)
        mesh.add_face(b12, b11, a11)
        mesh.add_face(b12, a11, a12)

def make_pipe_square_mesh(mesh, p0, p1, p2=[1.0, 0.0, 0.0], r1=1.0, r2=2.0, n=3):
    p0 = np.array(p0)
    p1 = np.array(p1)
    v1 = np.array([p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]])
    v2 = np.array([p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]])
    v3 = np.cross(v1, v2)
    if np.linalg.norm(v3) == 0:
        return
    v3_u = v3 / np.linalg.norm(v3)
    delta = 2.0 * np.pi / n
    rmat = rotation_matrix(v1, delta)
    o1 = mesh.add_vertex(p0)
    o2 = mesh.add_vertex(p1)
    aa1 = []
    aa2 = []
    bb1 = []
    bb2 = []
    theta = delta
    for i in range(n):
        # r of square = r2 * min(1.0 / abs(cos(theta)), 1.0 / abs(sin(theta)))
        r2_new = r2 * min(1.0 / abs(cos(theta)), 1.0 / abs(sin(theta)))
        theta += delta
        v3_u = np.dot(rmat, np.array(v3_u).T).T
        aa1.append(mesh.add_vertex(p0 + v3_u * r1))
        aa2.append(mesh.add_vertex(p0 + v3_u * r2_new))
        bb1.append(mesh.add_vertex(p1 + v3_u * r1))
        bb2.append(mesh.add_vertex(p1 + v3_u * r2_new))

    for i in range(n):
        a11 = aa1[i - 1]
        a12 = aa1[i]
        a21 = aa2[i - 1]
        a22 = aa2[i]
        b11 = bb1[i - 1]
        b12 = bb1[i]
        b21 = bb2[i - 1]
        b22 = bb2[i]
        mesh.add_face(a11, a21, a12)
        mesh.add_face(a12, a21, a22)
        mesh.add_face(a21, b21, a22)
        mesh.add_face(a22, b21, b22)
        mesh.add_face(b22, b21, b11)
        mesh.add_face(b22, b11, b12)
        mesh.add_face(b12, b11, a11)
        mesh.add_face(b12, a11, a12)

def make_rod_ellipse_mesh(mesh, p0, p1, p2=[1.0, 0.0, 0.0], a1=1.0, b1=4.0, n=64):
    p0 = np.array(p0)
    p1 = np.array(p1)
    v1 = np.array([p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]])
    v2 = np.array([p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]])
    v3 = np.cross(v1, v2)
    if np.linalg.norm(v3) == 0:
        return
    v3_u = v3 / np.linalg.norm(v3)
    delta = 2.0 * np.pi / n
    rmat = rotation_matrix(v1, delta)
    o1 = mesh.add_vertex(p0)
    o2 = mesh.add_vertex(p1)
    aa = []
    bb = []
    theta = delta
    for i in range(n):
        # ellipse r = a*b/sqrt((b*cos(theta))**2 + (a*sin(theta))**2)
        r1_new = a1 * b1 / sqrt((b1*cos(theta))**2 + (a1*sin(theta))**2)
        theta += delta
        v3_u = np.dot(rmat, np.array(v3_u).T).T
        aa.append(mesh.add_vertex(p0 + v3_u * r1_new))
        bb.append(mesh.add_vertex(p1 + v3_u * r1_new))

    for i in range(n):
        a1 = aa[i - 1]
        a2 = aa[i]
        b1 = bb[i - 1]
        b2 = bb[i]
        mesh.add_face(o1, a1, a2)
        mesh.add_face(o2, b2, b1)
        mesh.add_face(a2, a1, b1)
        mesh.add_face(b2, a2, b1)

def make_pipe_ellipse_mesh(mesh, p0, p1, p2=[1.0, 0.0, 0.0], a1=1.0, b1=4.0, a2=4.0, b2=16, n=64):
    p0 = np.array(p0)
    p1 = np.array(p1)
    v1 = np.array([p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]])
    v2 = np.array([p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]])
    v3 = np.cross(v1, v2)
    if np.linalg.norm(v3) == 0:
        return
    v3_u = v3 / np.linalg.norm(v3)
    delta = 2.0 * np.pi / n
    rmat = rotation_matrix(v1, delta)
    o1 = mesh.add_vertex(p0)
    o2 = mesh.add_vertex(p1)
    aa1 = []
    aa2 = []
    bb1 = []
    bb2 = []
    theta = delta
    for i in range(n):
        # ellipse r = a*b/sqrt((b*cos(theta))**2 + (a*sin(theta))**2)
        r1_new = a1 * b1 / sqrt((b1*cos(theta))**2 + (a1*sin(theta))**2)
        r2_new = a2 * b2 / sqrt((b2*cos(theta))**2 + (a2*sin(theta))**2)
        theta += delta
        v3_u = np.dot(rmat, np.array(v3_u).T).T
        aa1.append(mesh.add_vertex(p0 + v3_u * r1_new))
        aa2.append(mesh.add_vertex(p0 + v3_u * r2_new))
        bb1.append(mesh.add_vertex(p1 + v3_u * r1_new))
        bb2.append(mesh.add_vertex(p1 + v3_u * r2_new))

    for i in range(n):
        a11 = aa1[i - 1]
        a12 = aa1[i]
        a21 = aa2[i - 1]
        a22 = aa2[i]
        b11 = bb1[i - 1]
        b12 = bb1[i]
        b21 = bb2[i - 1]
        b22 = bb2[i]
        mesh.add_face(a11, a21, a12)
        mesh.add_face(a12, a21, a22)
        mesh.add_face(a21, b21, a22)
        mesh.add_face(a22, b21, b22)
        mesh.add_face(b22, b21, b11)
        mesh.add_face(b22, b11, b12)
        mesh.add_face(b12, b11, a11)
        mesh.add_face(b12, a11, a12)

def make_pipe_ellipse_part_mesh(mesh, p0, p1, p2=[1.0, 0.0, 0.0], a1=1.0, b1=4.0, a2=4.0, b2=16, n=64, m=32):
    p0 = np.array(p0)
    p1 = np.array(p1)
    v1 = np.array([p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]])
    v2 = np.array([p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]])
    v3 = np.cross(v1, v2)
    if np.linalg.norm(v3) == 0:
        return
    v3_u = v3 / np.linalg.norm(v3)
    delta = 2.0 * np.pi / n
    rmat = rotation_matrix(v1, delta)
    o1 = mesh.add_vertex(p0)
    o2 = mesh.add_vertex(p1)
    aa1 = []
    aa2 = []
    bb1 = []
    bb2 = []
    theta = 0
    for i in range(m):
        # ellipse r = a*b/sqrt((b*cos(theta))**2 + (a*sin(theta))**2)
        r1_new = a1 * b1 / sqrt((b1*cos(theta))**2 + (a1*sin(theta))**2)
        r2_new = a2 * b2 / sqrt((b2*cos(theta))**2 + (a2*sin(theta))**2)
        aa1.append(mesh.add_vertex(p0 + v3_u * r1_new))
        aa2.append(mesh.add_vertex(p0 + v3_u * r2_new))
        bb1.append(mesh.add_vertex(p1 + v3_u * r1_new))
        bb2.append(mesh.add_vertex(p1 + v3_u * r2_new))
        theta += delta
        v3_u = np.dot(rmat, np.array(v3_u).T).T
    
    # two ends
    mesh.add_face(aa2[0], aa1[0], bb1[0])
    mesh.add_face(aa2[0], bb1[0], bb2[0])
    mesh.add_face(aa1[m-1], aa2[m-1], bb1[m-1])
    mesh.add_face(aa2[m-1], bb2[m-1], bb1[m-1])

    for i in range(1, m):
        a11 = aa1[i - 1]
        a12 = aa1[i]
        a21 = aa2[i - 1]
        a22 = aa2[i]
        b11 = bb1[i - 1]
        b12 = bb1[i]
        b21 = bb2[i - 1]
        b22 = bb2[i]
        mesh.add_face(a11, a21, a12)
        mesh.add_face(a12, a21, a22)
        mesh.add_face(a21, b21, a22)
        mesh.add_face(a22, b21, b22)
        mesh.add_face(b22, b21, b11)
        mesh.add_face(b22, b11, b12)
        mesh.add_face(b12, b11, a11)
        mesh.add_face(b12, a11, a12)

# generate cone mesh based on p0->p1
def make_cone_mesh(mesh, p0, p1, p2=[1.0, 0.0, 0.0], r=1.0, n=3):
    p0 = np.array(p0)
    p1 = np.array(p1)
    v1 = np.array([p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]])
    v2 = np.array([p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]])
    v3 = np.cross(v1, v2)
    if np.linalg.norm(v3) == 0:
        return
    v3_u = v3 / np.linalg.norm(v3)
    delta = 2.0 * np.pi / n
    rmat = rotation_matrix(v1, delta)
    o1 = mesh.add_vertex(p0)
    o2 = mesh.add_vertex(p1)
    bb = []
    for i in range(n):
        v3_u = np.dot(rmat, np.array(v3_u).T).T
        bb.append(mesh.add_vertex(p1 + v3_u * r))

    for i in range(n):
        b1 = bb[i - 1]
        b2 = bb[i]
        mesh.add_face(o2, b2, b1)
        mesh.add_face(b2, o1, b1)

def rotation_matrix(axis, theta):
    mat = np.eye(3,3)
    axis = axis/sqrt(np.dot(axis, axis))
    a = cos(theta/2.)
    b, c, d = -axis*sin(theta/2.)

    return np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
                  [2*(b*c+a*d), a*a+c*c-b*b-d*d, 2*(c*d-a*b)],
                  [2*(b*d-a*c), 2*(c*d+a*b), a*a+d*d-b*b-c*c]])

