from Game.graphic.cartesian import plane, vector, scalar
from Game.color import BLACK
import pygame as pg
from math import pi, atan2, sqrt


class shape:

    def __init__(self, positon: vector, limit_vertex: bool = True) -> None:
        self.position_vec = positon
        self.plane = plane(self.position_vec.space.window_size,
                           1, self.position_vec.space, False)
        self.update()

        self.vertices: list[vector] = []
        self.limit_vertex = limit_vertex

    def update(self):
        self.plane.center = self.position_vec.XY

    def rotate(self, angle):
        for vertex in self.vertices:
            vertex.rotate(angle)

    def scale(self, factor):
        lengths = [vertex.length for vertex in self.vertices]
        if factor > 1:
            if max(lengths) * factor <= self.vertices[0].length_max or \
                    not self.limit_vertex:
                for vertex in self.vertices:
                    vertex *= factor
        elif factor < 1:
            if min(lengths) * factor >= 1:
                for vertex in self.vertices:
                    vertex *= factor

    def show(self, window, color=BLACK, width=1, show_vertex=False):
        if show_vertex:
            # self.position_vec.show(window)
            for vertex in self.vertices:
                vertex.show(window)
        pg.draw.lines(window, color, True,
                      [vertex.XY for vertex in self.vertices], width)


class rectangle(shape):

    def __init__(self, size: tuple, positon: vector, set_limit=True) -> None:
        super().__init__(positon, set_limit)

        alpha1 = atan2(size[1]//2, size[0]//2)
        alpha2 = pi - alpha1
        angles = [alpha1, alpha2, -alpha2, -alpha1]
        length = sqrt((size[0]//2)**2 + (size[1]//2)**2)

        for a in angles:
            self.vertices.append(
                self.plane.createVector(x=length, y=0, set_limit=set_limit))
            self.vertices[-1].rotate(a)


class triangle(shape):

    def __init__(self, size: tuple, positon: vector, set_limit=True) -> None:
        super().__init__(positon, set_limit)

        angles = [pi/2, -pi+pi/6, -pi/6]

        for i, a in enumerate(angles):
            self.vertices.append(
                self.plane.createVector(x=size[i], y=0, set_limit=set_limit))
            self.vertices[-1].rotate(a)


class circle(shape):

    def __init__(self, radius, positon: vector, set_limit=True) -> None:
        super().__init__(positon, set_limit)

        self.vertices.append(
            self.plane.createVector(x=radius, y=0, set_limit=set_limit))

    def show(self, window, color=BLACK, width=1, show_vertex=False):
        if show_vertex:
            # self.position_vec.show(window)
            self.vertices[0].show(window)
        pg.draw.circle(window, color, self.plane.center,
                       self.vertices[0].length, width)
