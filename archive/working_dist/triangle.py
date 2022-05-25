from typing import List
import numpy as np
from camera import Camera, calc_dist


class Triangle():
    def __init__(self, vec_indexes: List[int]):
        self.vec_indexes = vec_indexes

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

    def set_dist(self, cam: Camera):
        cam_pos = cam.point[:3, :]
        self.dist = calc_dist(self.centroid - cam_pos)[0, 0]
