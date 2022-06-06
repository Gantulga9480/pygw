from Game.base import Game
from Game.graphic import CartesianPlane
from Game.physics import PolygonBody, TriangleBody, RectBody
from Game.physics.body import object_body
from Game.physics import Engine
import numpy as np
import pygame as pg
import random
import math


class Test(Game):

    def __init__(self,
                 title: str = 'PyGameDemo',
                 width: int = 1920,
                 height: int = 1080,
                 fps: int = 60,
                 flags: int = pg.FULLSCREEN | pg.HWSURFACE,
                 render: bool = True) -> None:
        super().__init__(title, width, height, fps, flags, render)

        self.plane = CartesianPlane(self.window, (width, height),
                                    unit_length=1)
        self.frames: list[object_body] = []
        self.bodies: list[object_body] = []

        y = height / 2
        for i in range(28):
            vec = self.plane.createVector(-width/2, y)
            self.frames.append(RectBody(1,
                                        0,
                                        CartesianPlane(self.window, (40, 40), vec),
                                        (40, 40)))
            vec = self.plane.createVector(width/2, y)
            self.frames.append(RectBody(1,
                                        0,
                                        CartesianPlane(self.window, (40, 40), vec),
                                        (40, 40)))
            y -= 40

        x = -width/2 + 40
        for i in range(47):
            vec = self.plane.createVector(x, height / 2)
            self.frames.append(RectBody(1,
                                        0,
                                        CartesianPlane(self.window, (40, 40), vec),
                                        (40, 40)))
            vec = self.plane.createVector(x, -height / 2)
            self.frames.append(RectBody(1,
                                        0,
                                        CartesianPlane(self.window, (40, 40), vec),
                                        (40, 40)))
            x += 40

        self.shape_size = 40
        self.shape_vertex = 4
        self.current_vec = self.plane.createVector(0, 0)
        self.current_shape = PolygonBody(0, 0,
                                         CartesianPlane(self.window, (40, 40),
                                                        self.current_vec),
                                         (self.shape_size,
                                          self.shape_size,
                                          self.shape_size,
                                          self.shape_size))
        self.current_shape.rotate(math.pi/4)

    def USR_eventHandler(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_c:
                self.create_shape()
            elif event.key == pg.K_s:
                self.bodies.append(self.current_shape)
                self.create_shape()
            elif event.key == pg.K_UP:
                self.current_shape.scale(1.1)
            elif event.key == pg.K_DOWN:
                self.current_shape.scale(1/1.1)
            elif event.key == pg.K_RIGHT:
                self.current_shape.rotate(0.1)
            elif event.key == pg.K_LEFT:
                self.current_shape.rotate(-0.1)
            elif event.key == pg.K_q:
                if self.shape_vertex > 2:
                    self.shape_vertex -= 1
                    self.create_shape()
            elif event.key == pg.K_e:
                self.shape_vertex += 1
                self.create_shape()

    def USR_loop(self):
        self.current_vec.x = self.plane.to_x(self.mouse_x)
        self.current_vec.y = self.plane.to_y(self.mouse_y)

    def USR_render(self):
        self.current_vec.show((0, 0, 0))
        self.current_shape.show((0, 0, 255))
        for frame in self.frames:
            frame.show((0, 0, 0), True)
        for body in self.bodies:
            body.show((255, 0, 0))
        self.set_title(f'fps {round(self.clock.get_fps())}')

    def create_shape(self):
        self.current_vec = self.plane.createVector(0, 0)
        size = tuple([self.shape_size for _ in range(self.shape_vertex)])
        self.current_shape = PolygonBody(0, 0,
                                         CartesianPlane(self.window, (40, 40),
                                                        self.current_vec),
                                         size)
        self.current_shape.rotate(math.pi/4)


Test().mainloop()
