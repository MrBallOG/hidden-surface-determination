from typing import List, Tuple
import numpy as np
from camera import Camera, calc_dist
from functools import cmp_to_key


class Triangle():
    def __init__(self, vec_3d_list: List[np.matrix], vec_indexes: List[int], cam: Camera):
        self.cam = cam
        self.vec_indexes = vec_indexes
        self.p1 = vec_3d_list[vec_indexes[0]]
        self.p2 = vec_3d_list[vec_indexes[1]]
        self.p3 = vec_3d_list[vec_indexes[2]]

        if self.p1 is not None and self.p2 is not None and self.p3 is not None:
            self.set_min_max_y()
            self.set_normal()
            self.set_plane()

    def set_min_max_y(self):
        self.min_y = min([self.p1[1, 0], self.p2[1, 0], self.p3[1, 0]])
        self.max_y = max([self.p1[1, 0], self.p2[1, 0], self.p3[1, 0]])

    def set_normal(self):
        u = self.p2 - self.p1
        v = self.p3 - self.p1

        x = u[1, 0] * v[2, 0] - u[2, 0] * v[1, 0]
        y = u[2, 0] * v[0, 0] - u[0, 0] * v[2, 0]
        z = u[0, 0] * v[1, 0] - u[1, 0] * v[0, 0]

        self.normal = np.mat(dtype=np.double, data=[x, y, z]).T

    def set_plane(self):
        normal = self.normal
        d = (-self.p1.T * normal)[0, 0]
        plane = np.mat(dtype=np.double, data=[
                       normal[0, 0], normal[1, 0], normal[2, 0], d]).T

        self.plane = plane / np.linalg.norm(plane)

    def point_in_triangle(self, x: float, y: float):
        d1 = sign((x, y), self.p1, self.p2)
        d2 = sign((x, y), self.p2, self.p3)
        d3 = sign((x, y), self.p3, self.p1)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)

    def get_z_at_x_y(self, x: float, y: float):
        return -((x * self.plane[0, 0] + y * self.plane[1, 0] + self.plane[3, 0]) / self.plane[2, 0])


def sign(p1: Tuple, p2: np.matrix, p3: np.matrix):
    return (p1[0] - p3[0, 0]) * (p2[1, 0] - p3[1, 0]) - (p2[0, 0] - p3[0, 0]) * (p1[1] - p3[1, 0])
