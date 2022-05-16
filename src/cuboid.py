from typing import List, Tuple
import numpy as np
from camera import Camera


class Cuboid:
    def __init__(self, points: List[np.matrix]):
        self.points = points

    def to_list_of_lines(self, cam: Camera, scale: int, center: np.matrix) -> List[List[Tuple[int, int]]]:
        projected_points = []
        lines = []

        for point in self.points:
            projected = cam.project_point(point)

            if projected is not None:
                projected = projected * scale + center
                projected_points.append(projected)

        if len(projected_points) >= 8:
            for i in range(4):
                lines.append([(projected_points[i][0, 0], projected_points[i][1, 0]), (
                    projected_points[(i + 1) % 4][0, 0], projected_points[(i + 1) % 4][1, 0])])
                lines.append([(projected_points[i + 4][0, 0], projected_points[i + 4][1, 0]),
                              (projected_points[(i + 1) % 4 + 4][0, 0], projected_points[(i + 1) % 4 + 4][1, 0])])
                lines.append([(projected_points[i][0, 0], projected_points[i][1, 0]),
                              (projected_points[i + 4][0, 0], projected_points[i + 4][1, 0])])

        return lines
