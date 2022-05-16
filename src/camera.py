import numpy as np


T_VAL = 0.1
T_POINTS = np.matrix(dtype=np.double, data=np.array([[T_VAL, 0, 0, 1],
                                                     [-T_VAL, 0, 0, 1],
                                                     [0, T_VAL, 0, 1],
                                                     [0, -T_VAL, 0, 1],
                                                     [0, 0, T_VAL, 1],
                                                     [0, 0, -T_VAL, 1]])).T
DIST = 0.1
ANGLE_INCR = 1/180 * np.pi


class Camera:
    def __init__(self):
        self.point = np.mat(dtype=np.double, data=[0, 0, 15, 1]).T
        self.rotation_matrix = np.mat(dtype=np.double, data=[[1, 0, 0, 0],
                                                             [0, 1, 0, 0],
                                                             [0, 0, 1, 0],
                                                             [0, 0, 0, 1]])
        self.rotation_matrix_inverse = self.rotation_matrix.copy()
        self.fov = 30
        self.scale = fov_to_scale(self.fov)
        self.projection_matrix = self._get_projection_matrix()

    def rotate_x_pos(self):
        self._rotate_x(1)

    def rotate_x_neg(self):
        self._rotate_x(-1)

    def rotate_y_pos(self):
        self._rotate_y(1)

    def rotate_y_neg(self):
        self._rotate_y(-1)

    def rotate_z_pos(self):
        self._rotate_z(1)

    def rotate_z_neg(self):
        self._rotate_z(-1)

    def _rotate_x(self, i):
        cos = np.cos(i * ANGLE_INCR)
        sin = np.sin(i * ANGLE_INCR)
        r_x = np.matrix(dtype=np.double, data=[[1, 0, 0, 0],
                                               [0, cos, sin, 0],
                                               [0, -sin, cos, 0],
                                               [0, 0, 0, 1]])
        self.rotation_matrix = r_x * self.rotation_matrix
        self.rotation_matrix_inverse = inverse_matrix(self.rotation_matrix)

    def _rotate_y(self, i):
        cos = np.cos(i * ANGLE_INCR)
        sin = np.sin(i * ANGLE_INCR)
        r_y = np.matrix(dtype=np.double, data=[[cos, 0, -sin, 0],
                                               [0, 1, 0, 0],
                                               [sin, 0, cos, 0],
                                               [0, 0, 0, 1]])
        self.rotation_matrix = r_y * self.rotation_matrix
        self.rotation_matrix_inverse = inverse_matrix(self.rotation_matrix)

    def _rotate_z(self, i):
        cos = np.cos(i * ANGLE_INCR)
        sin = np.sin(i * ANGLE_INCR)
        r_z = np.matrix(dtype=np.double, data=[[cos, sin, 0, 0],
                                               [-sin, cos, 0, 0],
                                               [0, 0, 1, 0],
                                               [0, 0, 0, 1]])
        self.rotation_matrix = r_z * self.rotation_matrix
        self.rotation_matrix_inverse = inverse_matrix(self.rotation_matrix)

    def _transform_world_to_cam(self, point: np.matrix) -> np.matrix:
        point_at_origin = subtract_points(point, self.point)
        return self._rotate_world_to_cam(point_at_origin)

    def _rotate_world_to_cam(self, point: np.matrix) -> np.matrix:
        return self.rotation_matrix * point

    def _rotate_cam_to_world(self, point: np.matrix) -> np.matrix:
        return self.rotation_matrix_inverse * point

    def translate_x_pos(self):
        self._translate(0)

    def translate_x_neg(self):
        self._translate(1)

    def translate_y_pos(self):
        self._translate(2)

    def translate_y_neg(self):
        self._translate(3)

    def translate_z_pos(self):
        self._translate(4)

    def translate_z_neg(self):
        self._translate(5)

    def _translate(self, i: int):
        rotated = self._rotate_cam_to_world(T_POINTS[:, i])
        self.point = add_points(self.point, rotated)

    def zoom_in(self):
        fov = self.fov
        if fov > 20:
            self.fov = fov - 10
            self.scale = fov_to_scale(self.fov)
            self.projection_matrix = self._get_projection_matrix()

    def zoom_out(self):
        fov = self.fov
        if fov < 100:
            self.fov = fov + 10
            self.scale = fov_to_scale(self.fov)
            self.projection_matrix = self._get_projection_matrix()

    def _get_projection_matrix(self):
        temp = 1 / (1 - DIST)
        return np.mat(dtype=np.double, data=[[self.scale, 0, 0, 0],
                                             [0, self.scale, 0, 0],
                                             [0, 0, temp, -DIST * temp],
                                             [0, 0, 1, 0]])

    def project_point(self, point: np.matrix) -> np.matrix:
        rotated = self._transform_world_to_cam(point)
        projected = self.projection_matrix * rotated
        w = projected[3, 0]

        if w > 0.00000000000001:
            return None

        return (projected / w)[:2, 0]


def deg_to_rad(deg: int):
    return deg / 180 * np.pi


def add_points(p1: np.matrix, p2: np.matrix) -> np.matrix:
    return np.mat(dtype=np.double, data=[p1[0, 0] + p2[0, 0], p1[1, 0] + p2[1, 0], p1[2, 0] + p2[2, 0], 1]).T


def subtract_points(p1: np.matrix, p2: np.matrix, ) -> np.matrix:
    return np.mat(dtype=np.double, data=[p1[0, 0] - p2[0, 0], p1[1, 0] - p2[1, 0], p1[2, 0] - p2[2, 0], 1]).T


def fov_to_scale(fov: int) -> np.double:
    return 1 / np.tan(deg_to_rad(fov / 2))


def inverse_matrix(m: np.matrix):
    return np.linalg.inv(m)
