from typing import List, Tuple
import numpy as np
from camera import Camera


POLYGON_POINTS_ORDERED = [[0, 1, 2, 3], [4, 0, 3, 7],
                          [1, 5, 6, 2], [4, 5, 6, 7],
                          [0, 1, 5, 4], [3, 2, 6, 7]]


class Cuboid:
    def __init__(self, points: List[np.matrix], color: Tuple):
        self.points = points
        self.color = color

    def to_list_of_polygons(self, cam: Camera, scale: int, center: np.matrix) -> List[List[Tuple[np.double, np.double, np.double]]]:
        projected_points = []
        polygons = []

        for point in self.points:
            projected = cam.project_point(point)

            if projected is not None:
                projected[:2] = projected[:2] * scale + center
                projected_points.append(projected)

        if len(projected_points) == 8:
            for ordered_points in POLYGON_POINTS_ORDERED:
                polygon = [self.color]

                for i in ordered_points:
                    polygon.append(
                        (projected_points[i][0, 0], projected_points[i][1, 0], projected_points[i][2, 0], projected_points[i][3, 0]))

                polygons.append(polygon)

        return polygons
