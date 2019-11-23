import numpy as np
from math import cos, sin, sqrt

# compute rotation matrix around given axis for angle theta
def rotation_matrix(axis, theta):
    mat = np.eye(3,3)
    axis = axis/sqrt(np.dot(axis, axis))
    a = cos(theta/2.)
    b, c, d = -axis*sin(theta/2.)

    return np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
                  [2*(b*c+a*d), a*a+c*c-b*b-d*d, 2*(c*d-a*b)],
                  [2*(b*d-a*c), 2*(c*d+a*b), a*a+d*d-b*b-c*c]])


class Point(object):
    def __init__(self, coords, n, t1, t2, front_angle=-1, angle_changed=False, border_point=False):
        self.coords = coords
        self.n = n
        self.t1 = t1
        self.t2 = t2
        self.front_angle = front_angle
        self.angle_changed = angle_changed
        self.border_point = border_point

# surface trianglulation according to Erich Hartmann's paper
# A marching method for the triangulation of surfaces
# The Visual Computer (1998) 14:95-108
class TriMesh(object):
    def __init__(self, f, fg, fbox=None):
        # list of vertex index
        self.vertex = []
        # list of edges
        self.edge = []
        # list of triangles
        self.triangle = []
        # index of vertex in front polygons
        self.front_polygons = [[]]
        # surface function
        self.f = f
        # gradient function
        self.fg = fg
        # boundary condition
        self.fbox = fbox
        # triangle edge length
        self.delta = None
        # checked point list for distance check
        self.check_point_set = set()

#    def compute_f(self, x, y, z):
#        return self.f(x, y, z)

    def get_edge_list(self):
        self.edge = []
        for t1 in self.triangle:
            self.edge.append([t1[0], t1[1]])
            self.edge.append([t1[1], t1[2]])
            self.edge.append([t1[2], t1[0]])
        return self.edge

    def update_front_angle(self, fp0):
        for i in range(len(fp0)):
            p0 = self.vertex[fp0[i]]
            if p0.angle_changed == False or p0.border_point == True:
                continue
            v1 = self.vertex[fp0[i - 1]].coords
            j = i + 1
            if j >= len(fp0):
                j = 0
            v2 = self.vertex[fp0[j]].coords
            #rmatrix = np.linalg.inv(np.column_stack((p0.n, p0.t1, p0.t2)))
            #P = O1 + x1 X1 + y1 Y1 + z1 Z1   and
            #P = O2 + x2 X2 + y2 Y2 + z2 Z2
            #[ O11 ]   [ X11  X12  X13 ][ x1 ]   [ O21 ]   [ X21  X22  X23 ][ x2 ]
            #[ O12 ] + [ Y11  Y12  Y13 ][ y1 ] = [ O22 ] + [ Y21  Y22  Y23 ][ y2 ]
            #[ O13 ]   [ Z11  Z12  Z13 ][ z1 ]   [ O23 ]   [ Z21  Z22  Z23 ][ z2 ]
            #O1 + M1 p1 = O2 + M2 p2
            #If your coordinate axes for each system are linearly independent, 
            # then M1 and M2 are invertible. If in addition they are orthogonal, 
            # then the inverse of each is just it's transpose! So we get:
            #p1 = Transpose[M1] (O2 - O1 + M2 p2) and similarly going the other way
            #p2 = Transpose[M2] (O1 - O2 + M1 p1)
            rmatrix = np.column_stack((p0.n, p0.t1, p0.t2))
            v1n = np.dot(rmatrix.T, (v1 - p0.coords)).T
            v2n = np.dot(rmatrix.T, (v2 - p0.coords)).T
            w1 = np.arctan2(v1n[2], v1n[1])
            w2 = np.arctan2(v2n[2], v2n[1])
            if w2 >= w1:
                w = w2 - w1
            else:
                w = w2 - w1 + np.pi*2
            #print w / np.pi
            p0.front_angle = w

    def find_min_front_angle(self, fp0):
        # find the min angle front point
        angle_min = 10000
        angle_min_i = -1
        for i in range(len(fp0)):
            p0 = self.vertex[fp0[i]]
            if p0.front_angle < angle_min:
                angle_min = p0.front_angle
                angle_min_i = i
        #print fp0, angle_min_i
        p0m_i = fp0[angle_min_i]
        p0m = self.vertex[p0m_i]
        return p0m_i, p0m, angle_min, angle_min_i

    def trianglulation_single_front_point(self, fp0, p0m_i, p0m, angle_min, angle_min_i):
        v1_i = fp0[angle_min_i - 1]
        v1 = self.vertex[v1_i].coords
        v2_i = angle_min_i + 1
        if v2_i >= len(fp0):
            v2_i = 0
        v2_i = fp0[v2_i]
        v2 = self.vertex[v2_i].coords
        # determine the number of triangles nt to be generated
        nt = int(3.0*angle_min/np.pi) + 1
        da = angle_min / nt
        # correct da for extreme cases
        if da < 0.8 and nt > 1:
            nt = nt - 1
            da = angle_min / nt
        if nt == 1 and da > 0.8 and np.linalg.norm(v1-v2) > 1.2 * self.delta:
            nt = 2
            da = da / 2
        if angle_min < 3 and (np.linalg.norm(v1-p0m.coords) <= 0.5 * self.delta or np.linalg.norm(v2-p0m.coords) <= 0.5 * self.delta):
            nt = 1
        #print nt, da / np.pi
        # generate the triangles
        if nt == 1:
            self.triangle.append((v1_i, v2_i, p0m_i))
            fp0.remove(p0m_i)
        else:
            # projection to tengent plane at p0m
            rmatrix = np.column_stack((p0m.n, p0m.t1, p0m.t2))
            v1n = np.dot(rmatrix.T, (v1 - p0m.coords).T).T
            v1n[0] = 0
            q0 = p0m.coords + np.dot(rmatrix, v1n.T).T
            v1m = q0 - p0m.coords
            v1m = v1m / np.linalg.norm(v1m)
            rmat = rotation_matrix(p0m.n, -da)
            nn = len(self.vertex)
            for j in range(nt - 1):
                v1m = np.dot(rmat, v1m.T).T
                qj = p0m.coords + self.delta * v1m
                pj = self.procedure_surface_point(qj) 
                self.vertex.append(pj)
                #self.vertex.append(Point(qj, [], [], []))
                if j == 0:
                    self.triangle.append((v1_i, nn, p0m_i))
                else:
                    #print nn + j - 1, nn + j, p0m_i
                    self.triangle.append((nn + j - 1, nn + j, p0m_i))
            self.triangle.append((nn + nt - 2, v2_i, p0m_i))
            # renew the actual front polygon
            #fp0.remove(p0m_i)
            fp0_insert = []
            for j in range(nt - 1):
                self.vertex[nn + j].angle_changed = True
                fp0_insert.append(nn + j)
            self.front_polygons[0] = fp0[0:angle_min_i] + fp0_insert + fp0[angle_min_i + 1:]
            # reset angle_changed
            self.vertex[v1_i].angle_changed = True
            self.vertex[v2_i].angle_changed = True

    def build_triangle(self, starting_point, delta=0.3, init_front_polygons=[], init_vertex=[]):
        self.delta = delta
        ## step 0
        if len(init_front_polygons) == 0:
            p1 = self.procedure_surface_point(starting_point)
            #print starting_point, p0
            self.vertex.append(p1)
            for j in range(6):
                qj = p1.coords + delta * np.cos(np.pi * j / 3.0) * p1.t1 + delta * np.sin(np.pi * j / 3.0) * p1.t2
                pj = self.procedure_surface_point(qj)
                self.vertex.append(pj)
                pj.angle_changed=True
                self.front_polygons[0].append(j + 1)
                # make first 6 triangles
                if j < 5:
                    self.triangle.append((0, j + 1, j + 2))
                else:
                    self.triangle.append((0, 6, 1))
        else:
            self.front_polygons = init_front_polygons
            for v1 in init_vertex:
                pj = self.procedure_surface_point(v1)
                pj.angle_changed=True
                self.vertex.append(pj)
            for fpt in self.front_polygons:
                self.update_front_angle(fpt)

        # main marching cycle
        while sum([len(fp1) for fp1 in self.front_polygons]) > 0:
            # switch front polugon every 100 cycle
            if (len(self.vertex) + 1) % 100 == 0 and len(self.front_polygons) > 1:
                #print self.front_polygons
                fpt = self.front_polygons.pop(0)
                self.front_polygons.append(fpt)
            ## step 1 update front angles
            fp0 = self.front_polygons[0]
            if len(fp0) < 1:
                self.front_polygons.pop(0)
                continue
            self.update_front_angle(fp0)

            ## step 2 distance check to prevent overlapping
            # find the min angle front point
            p0m_i, p0m, angle_min, angle_min_i = self.find_min_front_angle(fp0)
            #print p0m_i, p0m, angle_min, angle_min_i
            # check boundary condition
            if self.fbox and not self.fbox(p0m.coords):
                p0m.front_angle = 100000
                p0m.border_point = True
                fp0.remove(p0m_i)
                continue
            
            # apply distance check only for mininum front angle > 60
            if angle_min >= np.pi / 3:
                dcheck = False
                for i in range(-3, len(fp0) - 3):
                    for j in range(i + 3, len(fp0) + min(i - 1 , 0)):
                        vi = fp0[i]
                        vj = fp0[j]
                        if vi not in self.check_point_set and vj not in self.check_point_set:
                            if np.linalg.norm(self.vertex[vi].coords - self.vertex[vj].coords) < self.delta:
                                if len(fp0[i:j + 1]) < 3:
                                    continue
                                self.front_polygons[0] = fp0[0:i + 1] + fp0[j:]
                                self.front_polygons.append(fp0[i:j + 1])
                                self.check_point_set.add(vi)
                                self.check_point_set.add(vj)
                                dcheck = True
                                break
                    if dcheck:
                        break
                if dcheck:
                    if len(self.front_polygons[0]) == 3:
                        v3 = self.front_polygons.pop(0)
                        #print v3
                        self.triangle.append((v3[2], v3[1], v3[0]))
                        continue
                    fp0 = self.front_polygons[0]
                    self.update_front_angle(fp0)
                    p0m_i, p0m, angle_min, angle_min_i = self.find_min_front_angle(fp0)
                else:
                    ucheck = False
                    for i in range(len(fp0)):
                        for fpj in range(1, len(self.front_polygons)):
                            for j in range(len(self.front_polygons[fpj])):
                                vi = fp0[i]
                                vj = self.front_polygons[fpj][j]
                                if vi not in self.check_point_set and vj not in self.check_point_set:
                                    if np.linalg.norm(self.vertex[vi].coords - self.vertex[vj].coords) < self.delta:
                                        fpt = self.front_polygons.pop(fpj)
                                        vim1 = fp0[i - 1]
                                        vip1 = fp0[i + 1]
                                        vjm1 = fpt[j - 1]
                                        vjp1 = fpt[j + 1]
                                        #print vim1, vi, vip1
                                        #print vjm1, vj, vjp1
                                        if np.linalg.norm(self.vertex[vim1].coords - self.vertex[vj].coords) < np.linalg.norm(self.vertex[vi].coords - self.vertex[vjp1].coords):
                                            self.triangle.append((vi, vim1, vj))
                                            self.triangle.append((vj, vim1, vjp1))
                                        else:
                                            self.triangle.append((vi, vim1, vjp1))
                                            self.triangle.append((vj, vi, vjp1))
                                        if np.linalg.norm(self.vertex[vi].coords - self.vertex[vjm1].coords) < np.linalg.norm(self.vertex[vip1].coords - self.vertex[vj].coords):
                                            self.triangle.append((vj, vjm1, vi))
                                            self.triangle.append((vi, vjm1, vip1))
                                        else:
                                            self.triangle.append((vj, vjm1, vip1))
                                            self.triangle.append((vi, vj, vip1))
                                        # update front angles
                                        self.vertex[vim1].angle_changed = True
                                        self.vertex[vip1].angle_changed = True
                                        self.vertex[vjm1].angle_changed = True
                                        self.vertex[vjp1].angle_changed = True
                                        self.check_point_set.add(vi)
                                        self.check_point_set.add(vjm1)
                                        self.check_point_set.add(vjp1)
                                        self.check_point_set.add(vj)
                                        self.check_point_set.add(vjm1)
                                        self.check_point_set.add(vjp1)
                                        self.front_polygons[0] = fp0[:i] + fpt[j + 1:] + fpt[:j] + fp0[i + 1:]
                                        ucheck = True
                                        break
                            if ucheck:
                                break
                        if ucheck:
                            break
                    if ucheck:
                        # recalculate front angle 
                        fp0 = self.front_polygons[0]
                        self.update_front_angle(fp0)
                        continue
                        #self.update_front_angle(fp0)
                        #p0m_i, p0m, angle_min, angle_min_i = self.find_min_front_angle(fp0)

            ## step 3 trianglulation at front point with minimal angle
            self.trianglulation_single_front_point(fp0, p0m_i, p0m, angle_min, angle_min_i)

            ## step 4 check the size of first front polygon == 3?
            #print self.front_polygons
            if len(self.front_polygons[0]) == 3:
                v3 = self.front_polygons.pop(0)
                self.triangle.append((v3[2], v3[1], v3[0]))
            if len(self.vertex) > 100000:
                return

    def procedure_surface_point(self, q, delta=0.000000001):
        u0 = np.array(q)
        g0 = self.fg(u0)
        d = 1.0
        while d > delta:
            u1 = u0 - self.f(u0) / (np.dot(g0, g0.T)) * g0
            d = np.linalg.norm(u1 - u0)
            u0 = u1
            g0 = self.fg(u0)

        n0 = g0 / np.linalg.norm(g0)
        if n0[0] > 0.5 or n0[1] > 0.5:
            t1 = np.array([n0[1], -n0[0], 0])
        else:
            t1 = np.array([-n0[2], 0, n0[0]])
        t1 = t1 / np.linalg.norm(t1)
        t2 = np.cross(n0, t1)
        return Point(u0, n0, t1, t2)

