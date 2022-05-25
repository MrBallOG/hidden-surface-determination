from typing import List, Tuple
import numpy as np
from functools import cmp_to_key
from triangle import Triangle


def depth_sort(triangles: List[Triangle]):
    triangles.sort(key=lambda triangle: triangle.dist, reverse=True)


# def compare(pol_1: List[Tuple[np.double, np.double, np.double]], pol_2: List[Tuple[np.double, np.double, np.double]]):
#     min_dist_1 = min(pol_1[1:], key=lambda point: point[3])[3]
#     min_dist_2 = min(pol_2[1:], key=lambda point: point[3])[3]

#     if min_dist_1 < min_dist_2:
#         return 1
#     elif min_dist_1 > min_dist_2:
#         return -1

#     max_dist_1 = max(pol_1[1:], key=lambda point: point[3])[3]
#     max_dist_2 = max(pol_2[1:], key=lambda point: point[3])[3]

#     if max_dist_1 < max_dist_2:
#         return 1
#     elif max_dist_1 > max_dist_2:
#         return -1
#     else:
#         return 0
