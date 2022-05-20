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

        self.plane = CartesianPlane((width, height), 1, None)

        self.shapes: list[list[Vector2d, polygon]] = []
        self.current_vertex_count = 5

        self.create_shape()

    def USR_eventHandler(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                self.current_shape.scale(1.1)
            elif event.key == pg.K_DOWN:
                self.current_shape.scale(1/1.1)
            if event.key == pg.K_s:
                self.shapes.append([self.current_vector, self.current_shape])
                self.create_shape()
            if event.key == pg.K_LEFT:
                self.current_shape.rotate(0.1)
            elif event.key == pg.K_RIGHT:
                self.current_shape.rotate(-0.1)

    def USR_loop(self):
        self.current_vector.x = self.plane.to_x(self.mouse_x)
        self.current_vector.y = self.plane.to_y(self.mouse_y)

    def USR_render(self):
        self.plane.show(self.window)
        self.current_vector.show(self.window, BLUE)
        self.current_shape.show(self.window, BLACK)
        for shape in self.shapes:
            shape[1].show(self.window, (0, 255, 0))

    def create_shape(self):
        shape_size = 100
        self.current_vector = Vector2d(self.plane, 1, 1, 0, 0)
        self.current_shape_plane = CartesianPlane((500, 500),
                                                  1, self.current_vector)
        self.current_shape = polygon(self.current_shape_plane,
                                     self.current_vertex_count,
                                     shape_size)


Environment().mainloop()
