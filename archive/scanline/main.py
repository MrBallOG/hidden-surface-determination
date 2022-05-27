from typing import List
import pygame as pg
import numpy as np
from sys import argv
from reader import read_obj_file
from camera import Camera, WIDTH, HEIGHT, SCALE, CENTER
from triangle import Triangle
from hidden_surface_determination import depth_sort
from timeit import default_timer as tim


def main():
    black = (30, 30, 30)
    white = (255, 255, 255)
    yellow = (249, 215, 28)
    green = (0, 128, 0)
    red = (237, 28, 36)

    pg.init()
    pg.display.set_caption("3d projection")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    cam = Camera()
    objects = ["teapot", "cube", "sphere"]
    choice = int(argv[1]) if len(argv) > 1 else 0
    vec_3d_list, faces = read_obj_file(f"../obj/{objects[choice]}.obj")
    vec_3d_list_len = len(vec_3d_list)
    triangles: List[Triangle] = []

    np.set_printoptions(precision=3, suppress=True)
    for i, face in enumerate(faces):
        # if i == 3 or i == 9:
        triangle = Triangle(vec_3d_list, face, cam)
        triangles.append(triangle)
        # print("Normal", triangle.normal.T)
        # print("Plane", triangle.plane.T)
        # print("Centroid", triangle.centroid.T, "\n")

    # x = 1
    # for i, t1 in enumerate(triangles):
    #     for j, t2 in enumerate(triangles):
    #         if np.abs(t1.plane[0, 0] - t2.plane[0, 0]) == 0:
    #             if np.abs(t1.plane[1, 0] - t2.plane[1, 0]) == 0:
    #                 if np.abs(t1.plane[2, 0] - t2.plane[2, 0]) == 0:
    #                     if np.abs(t1.plane[3, 0] - t2.plane[3, 0]) == 0:
    #                         if np.array_equal(t1.plane, t2.plane):
    #                             print(x)
    #                             x += 1

    first_time = True
    # camera_moved = True
    wire_frame = True
    show_back_facing_triangles = True

    while True:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    return
                elif event.key == pg.K_z:
                    cam.zoom_in()
                elif event.key == pg.K_x:
                    cam.zoom_out()
                elif event.key == pg.K_c:
                    wire_frame = not wire_frame
                elif event.key == pg.K_v:
                    show_back_facing_triangles = not show_back_facing_triangles

        keys = pg.key.get_pressed()

        if keys[pg.K_d] > 0:
            cam.translate_x_neg()
            # camera_moved = True
        if keys[pg.K_a] > 0:
            cam.translate_x_pos()
            # camera_moved = True
        if keys[pg.K_w] > 0:
            cam.translate_y_pos()
            # camera_moved = True
        if keys[pg.K_s] > 0:
            cam.translate_y_neg()
            # camera_moved = True
        if keys[pg.K_q] > 0:
            cam.translate_z_pos()
            # camera_moved = True
        if keys[pg.K_e] > 0:
            cam.translate_z_neg()
            # camera_moved = True
        if keys[pg.K_k] > 0:
            cam.rotate_x_neg()
        if keys[pg.K_i] > 0:
            cam.rotate_x_pos()
        if keys[pg.K_l] > 0:
            cam.rotate_y_pos()
        if keys[pg.K_j] > 0:
            cam.rotate_y_neg()
        if keys[pg.K_u] > 0:
            cam.rotate_z_pos()
        if keys[pg.K_o] > 0:
            cam.rotate_z_neg()
        if not first_time:
            if len(pg.event.get()) == 0 and sum(_ for _ in keys) == 0:
                continue
        else:
            first_time = False

        screen.fill(black)

        triangles_to_project: List[Triangle] = []
        vec_3d_dict = {}

        if show_back_facing_triangles:
            for i in range(vec_3d_list_len):
                vec_3d_dict[i] = cam.project_point(vec_3d_list[i])

            for triangle in triangles:
                triangles_to_project.append(
                    Triangle(vec_3d_dict, triangle.vec_indexes, cam))
        else:
            vec_indexes = set()
            triangle_indexes = []

            for i, triangle in enumerate(triangles):
                p1 = vec_3d_list[triangle.vec_indexes[0]]
                p1_in_cam_world = p1 - cam.point[:3, :]
                dot = p1_in_cam_world.T * triangle.normal

                if dot < 0:
                    triangle_indexes.append(i)
                    vec_indexes.update(triangle.vec_indexes)

            for i in vec_indexes:
                vec_3d_dict[i] = cam.project_point(vec_3d_list[i])

            for i in triangle_indexes:
                triangles_to_project.append(
                    Triangle(vec_3d_dict, triangles[i].vec_indexes, cam))

        # # if camera_moved:
        # #     set_dists(triangles_to_project)
        # #     camera_moved = False

        s = tim()

        triangles_to_project.sort(key=lambda triangle: triangle.max_y)
        pixel_array = pg.PixelArray(screen)

        for y in range(HEIGHT):
            y3d = y_to_3d(y)
            triangles_at_y = [
                t for t in triangles_to_project if t.p1 is not None and t.p2 is not None and t.p3 is not None and t.max_y >= y3d and t.min_y <= y3d]

            if len(triangles_at_y) == 0:
                continue

            for x in range(WIDTH):
                x3d = x_to_3d(x)
                triangles_at_px = [
                    t for t in triangles_at_y if t.point_in_triangle(x3d, y3d)]
                triangles_at_px_len = len(triangles_at_px)

                if triangles_at_px_len == 0:
                    continue

                closest_triangle = triangles_at_px[0]
                closest_distance = closest_triangle.get_z_at_x_y(x3d, y3d)

                for i in range(1, triangles_at_px_len):
                    distance = triangles_at_px[i].get_z_at_x_y(x3d, y3d)

                    if distance < closest_distance:
                        closest_distance = distance
                        closest_triangle = triangles_at_px[i]

                pixel_array[x, y] = yellow

        e = tim()

        print((e-s) / (HEIGHT * WIDTH))
        print((e-s))

        print("DONE")

        # depth_sort(triangles_to_project)

        # for triangle in triangles_to_project:
        #     p1 = triangle.p1
        #     p2 = triangle.p2
        #     p3 = triangle.p3

        #     if p1 is None or p2 is None or p3 is None:
        #         continue

        #     p1 = p1[:2, 0] * SCALE + CENTER
        #     p2 = p2[:2, 0] * SCALE + CENTER
        #     p3 = p3[:2, 0] * SCALE + CENTER

        #     p1 = (p1[0, 0], p1[1, 0])
        #     p2 = (p2[0, 0], p2[1, 0])
        #     p3 = (p3[0, 0], p3[1, 0])

        #     pg.draw.polygon(screen, yellow, [p1, p2, p3])

        #     if wire_frame:
        #         pg.draw.line(screen, black, p1, p2)
        #         pg.draw.line(screen, black, p2, p3)
        #         pg.draw.line(screen, black, p1, p3)
        pixel_array.close()
        pg.display.flip()


def set_dists(triangles: List[Triangle]):
    for triangle in triangles:
        triangle.set_dist()


def y_to_3d(y: int) -> float:
    return 2 * y / HEIGHT - 1


def x_to_3d(x: int) -> float:
    return 2 * x / WIDTH - 1


main()
