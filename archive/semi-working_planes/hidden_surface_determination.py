from typing import List
import numpy as np
from functools import cmp_to_key
from triangle import Triangle


def depth_sort(triangles: List[Triangle]):
    triangles.sort(key=cmp_to_key(compare))


def compare(t1: Triangle, t2: Triangle):
    plane_t1 = t1.plane
    plane_t2 = t2.plane

    if np.array_equal(plane_t1, plane_t2):
        return 0

    dot_cam = (t1.cam.point.T * plane_t1)[0, 0]
    p1, p2, p3 = (t2.vec_3d_list[i] for i in t2.vec_indexes)
    dot_p1 = dot_3d_and_4d(p1, plane_t1)
    dot_p2 = dot_3d_and_4d(p2, plane_t1)
    dot_p3 = dot_3d_and_4d(p3, plane_t1)

    # print("dot t2  ", dot_t2)
    # print("centroid", t2.centroid)
    # print("plane   ", plane)

    triangle_on_same_side_neg = dot_p1 <= 0 and dot_p2 <= 0 and dot_p3 <= 0
    triangle_on_same_side_pos = dot_p1 >= 0 and dot_p2 >= 0 and dot_p3 >= 0

    if triangle_on_same_side_neg and dot_cam < 0:
        return -1
    elif triangle_on_same_side_pos and dot_cam > 0:
        return -1
    elif triangle_on_same_side_neg and dot_cam > 0:
        return 1
    elif triangle_on_same_side_pos and dot_cam < 0:
        return 1

    dot_cam = (t1.cam.point.T * plane_t2)[0, 0]
    p1, p2, p3 = (t1.vec_3d_list[i] for i in t1.vec_indexes)
    dot_p1 = dot_3d_and_4d(p1, plane_t2)
    dot_p2 = dot_3d_and_4d(p2, plane_t2)
    dot_p3 = dot_3d_and_4d(p3, plane_t2)

    triangle_on_same_side_neg = dot_p1 <= 0 and dot_p2 <= 0 and dot_p3 <= 0
    triangle_on_same_side_pos = dot_p1 >= 0 and dot_p2 >= 0 and dot_p3 >= 0

    if triangle_on_same_side_neg and dot_cam < 0:
        return 1
    elif triangle_on_same_side_pos and dot_cam > 0:
        return 1
    elif triangle_on_same_side_neg and dot_cam > 0:
        return -1
    elif triangle_on_same_side_pos and dot_cam < 0:
        return -1
    else:
        return 0

    # else:
    #     return 0

    # if dot_t2 < 0 and dot_cam < 0:
    #     return -1
    # elif dot_t2 > 0 and dot_cam > 0:
    #     return -1
    # else:
    #     return 1

    # if dot_t2 < 0 and dot_cam < 0:
    #     return -1
    # elif dot_t2 > 0 and dot_cam > 0:
    #     return -1
    # elif dot_t2 < 0 and dot_cam > 0:
    #     return 1
    # elif dot_t2 > 0 and dot_cam < 0:
    #     return 1
    # else:
    #     return 0  # 1 oznacza ze pierwszy lepszy, czyli wstawi na koiec listy ten pierwszy


def dot_3d_and_4d(vec_3d: np.matrix, vec_4d: np.matrix):
    return (vec_3d.T * vec_4d[:3, 0])[0, 0] + vec_4d[3, 0]


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
