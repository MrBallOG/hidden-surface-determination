from typing import List
import numpy as np
import pygame as pg
from camera import Camera
from cuboid import Cuboid
from hidden_surface_determination import depth_sort


def main():
    width, height = 1000, 800
    black = (30, 30, 30)
    white = (255, 255, 255)
    yellow = (249, 215, 28)
    green = (0, 128, 0)
    red = (237, 28, 36)

    cam = Camera()
    pg.init()
    pg.display.set_caption("3d projection")
    screen = pg.display.set_mode((width, height))
    clock = pg.time.Clock()
    center = np.mat(dtype=np.double, data=[width / 2, height / 2]).T
    scale = 300

    cuboids: List[Cuboid] = []
    cuboids.append(Cuboid([np.mat(dtype=np.double, data=[-1, -1, 1]).T,
                           np.mat(dtype=np.double, data=[1, -1, 1]).T,
                           np.mat(dtype=np.double, data=[1, 1, 1]).T,
                           np.mat(dtype=np.double, data=[-1, 1, 1]).T,
                           np.mat(dtype=np.double, data=[-1, -1, -1]).T,
                           np.mat(dtype=np.double, data=[1, -1, -1]).T,
                           np.mat(dtype=np.double, data=[1, 1, -1]).T,
                           np.mat(dtype=np.double, data=[-1, 1, -1]).T], white))
    cuboids.append(Cuboid([np.mat(dtype=np.double, data=[-1, -1, 1-5]).T,
                           np.mat(dtype=np.double, data=[1, -1, 1-5]).T,
                           np.mat(dtype=np.double, data=[0.5, 1, 0.5-5]).T,
                           np.mat(dtype=np.double, data=[-0.5, 1, 0.5-5]).T,
                           np.mat(dtype=np.double, data=[-1, -1, -1-5]).T,
                           np.mat(dtype=np.double, data=[1, -1, -1-5]).T,
                           np.mat(dtype=np.double, data=[0.5, 1, -0.5-5]).T,
                           np.mat(dtype=np.double, data=[-0.5, 1, -0.5-5]).T], yellow))
    cuboids.append(Cuboid([np.mat(dtype=np.double, data=[-1-6, -1, 1-5]).T,
                           np.mat(dtype=np.double, data=[1-6, -1, 1-5]).T,
                           np.mat(dtype=np.double, data=[1-6, 1+1, 1-5]).T,
                           np.mat(dtype=np.double, data=[-1-6, 1+1, 1-5]).T,
                           np.mat(dtype=np.double, data=[-1-6, -1, -1-5]).T,
                           np.mat(dtype=np.double, data=[1-6, -1, -1-5]).T,
                           np.mat(dtype=np.double, data=[1-6, 1+1, -1-5]).T,
                           np.mat(dtype=np.double, data=[-1-6, 1+1, -1-5]).T], green))
    # cuboids.append(Cuboid([np.mat(dtype=np.double, data=[-1-6, -1, 1+3]).T,
    #                        np.mat(dtype=np.double, data=[1-6, -1, 1+3]).T,
    #                        np.mat(dtype=np.double, data=[1-6, 1+4, 1+3]).T,
    #                        np.mat(dtype=np.double, data=[-1-6, 1+4, 1+3]).T,
    #                        np.mat(dtype=np.double, data=[-1-6, -1, -1]).T,
    #                        np.mat(dtype=np.double, data=[1-6, -1, -1]).T,
    #                        np.mat(dtype=np.double, data=[1-6, 1+4, - 1]).T,
    #                        np.mat(dtype=np.double, data=[-1-6, 1+4, -1]).T], red))

    first_time = True

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
        keys = pg.key.get_pressed()

        if keys[pg.K_d] > 0:
            cam.translate_x_neg()
        if keys[pg.K_a] > 0:
            cam.translate_x_pos()
        if keys[pg.K_w] > 0:
            cam.translate_y_pos()
        if keys[pg.K_s] > 0:
            cam.translate_y_neg()
        if keys[pg.K_q] > 0:
            cam.translate_z_pos()
        if keys[pg.K_e] > 0:
            cam.translate_z_neg()
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

        polygons = []

        for cuboid in cuboids:
            polygons.extend(cuboid.to_list_of_polygons(cam, scale, center))

        depth_sort(polygons)

        for polygon in polygons:
            pg.draw.polygon(screen,
                            polygon[0],
                            list(map(lambda _: _[:2], polygon))[1:])

            for i in range(1, len(polygon)):
                if i == len(polygon) - 1:
                    pg.draw.line(screen, black, polygon[1][:2], polygon[i][:2])
                else:
                    pg.draw.line(
                        screen, black, polygon[i][:2], polygon[i+1][:2])

        pg.display.update()


main()
