from math import sqrt
from solid import *

len_mult = 1000

def get_tetrahedron():
    a = [1, 0, 0]
    b = [0, 1, 0]
    c = [0, 0, 1]
    d = [0, 0, 0]
    return [a,b,c,d], [[0,1,2],[0,1,3],[1,2,3],[0,2,3]]


def midpoint(a, b):
    return [(a[0]+b[0])*0.5, (a[1]+b[1])*0.5, (a[2]+b[2])*0.5]


def len(v):
    x, y, z = v
    return sqrt(x**2 + y**2 + z**2)


def spherize(s):
    return [len_mult*coord/len(s) if len(s) != 0 else len_mult*coord for coord in s]


def iterate(points, faces):
    res_points, res_faces = [], []
    for counter, tr in enumerate(faces):
        a, b, c = [points[i] for i in tr]
        mid_ab = midpoint(a, b)
        mid_ac = midpoint(a, c)
        mid_bc = midpoint(b, c)
        res_points.extend([spherize(a), spherize(b), spherize(c), spherize(mid_ab), spherize(mid_ac), spherize(mid_bc)])
        #a, mid_ab, mid_ac
        #b, mid_ab, mid_bc
        #c, mid_ac, mid_bc
        #mid_ab, mid_bc, mid_ac
        res_faces.append([counter*6, counter*6+3, counter*6+4])
        res_faces.append([counter*6+1, counter*6+3, counter*6+5])
        res_faces.append([counter*6+2, counter*6+4, counter*6+5])
        res_faces.append([counter*6+3, counter*6+4, counter*6+5])
    return res_points, res_faces


def mirror(points, faces, axis = 'x'):
    result = []
    for point in points:
        if axis == 'x':
            result.append([point[0]*(-1), point[1], point[2]])
        elif axis == 'y':
            result.append([point[0], point[1]*(-1), point[2]])
    return result, faces

n = int(input("Enter number of iterations (values greater than 5 are not recommended):"))
triangles_points , triangles_faces = get_tetrahedron()
for i in range(n-1):
    triangles_points, triangles_faces = iterate(triangles_points, triangles_faces)
mirrored_x_points, mirrored_x_faces = mirror(triangles_points, triangles_faces, 'x')
mirrored_y_points, mirrored_y_faces = mirror(triangles_points, triangles_faces, 'y')
mirrored_xy_points, mirrored_xy_faces = mirror(mirrored_x_points, mirrored_x_faces, 'y')
obj = union()
obj.add(polyhedron(triangles_points, triangles_faces))
obj.add(polyhedron(mirrored_x_points, mirrored_x_faces))
obj.add(polyhedron(mirrored_y_points, mirrored_y_faces))
obj.add(polyhedron(mirrored_xy_points, mirrored_xy_faces))

scad_render_to_file(obj, 'output.scad')