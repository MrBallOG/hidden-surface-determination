from typing import List
import numpy as np
from camera import Camera, calc_dist
from functools import cmp_to_key


class Triangle():
    def __init__(self, vec_3d_list: List[np.matrix], vec_indexes: List[int], cam: Camera):
        self.vec_3d_list = vec_3d_list
        self.vec_indexes = vec_indexes
        self.cam = cam

    def set_centroid(self, vec_3d_list: List[np.matrix]):
        centroid = np.mat(dtype=np.double, data=[0, 0, 0]).T

        for i in range(3):
            vec_3d = vec_3d_list[self.vec_indexes[i]]
            centroid += vec_3d

        self.centroid = centroid / 3

    def set_normal(self, vec_3d_list: List[np.matrix]):
        p1, p2, p3 = (vec_3d_list[i] for i in self.vec_indexes)
        u = p2 - p1
        v = p3 - p1

        x = u[1, 0] * v[2, 0] - u[2, 0] * v[1, 0]
        y = u[2, 0] * v[0, 0] - u[0, 0] * v[2, 0]
        z = u[0, 0] * v[1, 0] - u[1, 0] * v[0, 0]

        self.normal = np.mat(dtype=np.double, data=[x, y, z]).T

    def set_dist(self):
        cam_pos = self.cam.point[:3, 0]
        self.dist = calc_dist(self.centroid - cam_pos)[0, 0]

    def set_plane(self, vec_3d_list: List[np.matrix]):
        p1 = vec_3d_list[self.vec_indexes[0]]
        normal = self.normal
        d = (-p1.T * normal)[0, 0]
        plane = np.mat(dtype=np.double, data=[
                       normal[0, 0], normal[1, 0], normal[2, 0], d]).T
        self.plane = plane / np.linalg.norm(plane)

        # print("p1", p1)
        # print("-p1.T", -p1.T)
        # print("normal", self.normal)
        # print("centroid", self.centroid)
        # print("plane", self.plane, "\n\n")
        # p1, p2, p3 = (vec_3d_list[i] for i in self.vec_indexes)
        # print(self.normal.T * (p2-p1), self.normal.T * (p3-p1))


# def my_cmp(a, b, c):
#     if a > b-c:
#         return 1
#     elif b > a:
#         return -1   # wstawia na poczatek listy
#     else:
#         return 0


# def sort_this(arr):
#     x = 1
#     arr.sort(key=cmp_to_key(my_cmp(c=x)))
