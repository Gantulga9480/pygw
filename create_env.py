from Game import *
from Game.graphic import *
from Game.math import *
from Game.physics import *
import numpy as np
import pygame as pg


class Environment(Game):

    def __init__(self,
                 title: str = 'ENV',
                 width: int = 1920,
                 height: int = 1080,
                 fps: int = 60,
                 flags: int = pg.FULLSCREEN | pg.HWSURFACE,
                 render: bool = True) -> None:
        super().__init__(title, width, height, fps, flags, render)

        self.plane = CartesianPlane(self.window, (width, height), unit_length=1)

        self.shapes: list[list[Vector2d, polygon]] = []
        self.current_vertex_count = 5

        self.create_shape()

    def USR_eventHandler(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_s:
                self.shapes.append([self.current_vector, self.current_shape])
                self.create_shape()
            if event.key == pg.K_q:
                self.current_vertex_count += 1
                self.create_shape()
            elif event.key == pg.K_e:
                if self.current_vertex_count > 3:
                    self.current_vertex_count -= 1
                    self.create_shape()

    def USR_loop(self):
        self.current_vector.x = self.plane.to_x(self.mouse_x)
        self.current_vector.y = self.plane.to_y(self.mouse_y)

        if self.keys[pg.K_UP]:
            self.current_shape.scale(1.1)
        elif self.keys[pg.K_DOWN]:
            self.current_shape.scale(1/1.1)
        if self.keys[pg.K_LEFT]:
            self.current_shape.rotate(0.05)
        elif self.keys[pg.K_RIGHT]:
            self.current_shape.rotate(-0.05)

    def USR_render(self):
        self.plane.show()
        self.current_vector.show(BLUE)
        self.current_shape.show(BLACK)
        for shape in self.shapes:
            shape[1].show((0, 255, 0))

    def create_shape(self):
        shape_size = 100
        self.current_vector = Vector2d(self.plane, 1, 1, 0, 0)
        self.current_shape_plane = CartesianPlane(self.window, (500, 500),
                                                  self.current_vector)
        self.current_shape = polygon_test(self.current_shape_plane,
                                          [200, 200, 10, 200, 200])


Environment().mainloop()
