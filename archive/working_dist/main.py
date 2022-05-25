from typing import List
import pygame as pg
from sys import argv
from reader import read_obj_file
from camera import Camera, WIDTH, HEIGHT
from triangle import Triangle
from hidden_surface_determination import depth_sort


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
    vec_3d_list, faces = read_obj_file(f"../../obj/{objects[choice]}.obj")
    triangles: List[Triangle] = []

    for face in faces:
        triangle = Triangle(face)
        triangle.set_centroid(vec_3d_list)
        triangle.set_normal(vec_3d_list)
        triangles.append(triangle)

    first_time = True
    camera_moved = True
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
            camera_moved = True
        if keys[pg.K_a] > 0:
            cam.translate_x_pos()
            camera_moved = True
        if keys[pg.K_w] > 0:
            cam.translate_y_pos()
            camera_moved = True
        if keys[pg.K_s] > 0:
            cam.translate_y_neg()
            camera_moved = True
        if keys[pg.K_q] > 0:
            cam.translate_z_pos()
            camera_moved = True
        if keys[pg.K_e] > 0:
            cam.translate_z_neg()
            camera_moved = True
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

        triangles_to_project = []
        vec_2d_dict = {}

        if show_back_facing_triangles:
            triangles_to_project = triangles

            for index in range(len(vec_3d_list)):
                vec_2d_dict[index] = cam.project_point(vec_3d_list[index])
        else:
            for triangle in triangles:
                p1 = vec_3d_list[triangle.vec_indexes[0]]
                p1_in_cam_world = p1 - cam.point[:3, :]
                dot = p1_in_cam_world.T * triangle.normal

                if dot < 0:
                    triangles_to_project.append(triangle)

            indexes_to_project = set()

            for triangle in triangles_to_project:
                indexes_to_project.update(triangle.vec_indexes)

            for index in indexes_to_project:
                vec_2d_dict[index] = cam.project_point(vec_3d_list[index])

        if camera_moved:
            set_dists(triangles_to_project, cam)
            camera_moved = False

        depth_sort(triangles_to_project)

        for triangle in triangles_to_project:
            p1, p2, p3 = (vec_2d_dict[i] for i in triangle.vec_indexes)

            if p1 is None or p2 is None or p3 is None:
                continue

            pg.draw.polygon(screen, yellow, [p1, p2, p3])

            if wire_frame:
                pg.draw.line(screen, black, p1, p2)
                pg.draw.line(screen, black, p2, p3)
                pg.draw.line(screen, black, p1, p3)

        pg.display.update()


def set_dists(triangles: List[Triangle], cam: Camera):
    for triangle in triangles:
        triangle.set_dist(cam)


main()
