import numpy as np
from math import cos, sin, sqrt

# generate mesh based on p0->p1
def make_mesh(mesh, p0, p1, p2=[1.0, 0.0, 0.0], r=1.0, n=3):
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
        mesh.add_face(o1, a2, a1)
        mesh.add_face(o2, b1, b2)
        mesh.add_face(a1, a2, b1)
        mesh.add_face(b1, a2, b2)

def rotation_matrix(axis, theta):
    mat = np.eye(3,3)
    axis = axis/sqrt(np.dot(axis, axis))
    a = cos(theta/2.)
    b, c, d = -axis*sin(theta/2.)

    return np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
                  [2*(b*c+a*d), a*a+c*c-b*b-d*d, 2*(c*d-a*b)],
                  [2*(b*d-a*c), 2*(c*d+a*b), a*a+d*d-b*b-c*c]])

# pose vector 6: translation x, y, z, rotation about x, y, z axis
def initial_pose(block1, pose):
    vv = block1.vertex
    translation = np.array(pose[0:3])
    theta_x = pose[3]
    theta_y = pose[4]
    theta_z = pose[5]
    print "translation {0} rotation x {1} y {2} z {3}".format(translation, theta_x, theta_y, theta_z)
    # rotate around x axis
    rmat = rotation_matrix(np.array([1, 0, 0]), theta_x)
    vv = np.dot(rmat, np.array(vv).T).T
    # rotate around y axis
    rmat = rotation_matrix(np.array([0, 1, 0]), theta_y)
    vv = np.dot(rmat, np.array(vv).T).T
    # rotate around z axis
    rmat = rotation_matrix(np.array([0, 0, 1]), theta_z)
    vv = np.dot(rmat, np.array(vv).T).T
    # translation
    vv = vv + translation
    block1.vertex = vv
