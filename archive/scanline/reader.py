import numpy as np


def read_obj_file(filename: str):
    vec_3d_list = []
    faces = []

    with open(filename, "r") as file:
        for line in file:
            if line.startswith("v "):
                x, y, z = line[2:].strip().split(" ")
                vec_3d = np.mat(dtype=np.double, data=[x, y, z]).T
                vec_3d_list.append(vec_3d)
            if line.startswith("f "):
                faces.append([int(index.split("/")[0]) - 1
                             for index in line[2:].strip().split(" ")])

    return vec_3d_list, faces
