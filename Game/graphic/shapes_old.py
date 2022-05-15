from Game.graphic.cartesian import CartesianPlane, Vector2d
from Game.color import BLACK
import pygame as pg
from math import pi, sqrt


class shape:

    def __init__(self, plane: CartesianPlane,
                 limit_vertex: bool = True) -> None:
        super(shape, self).__init__()
        self.plane = plane

        self.vertices: list[Vector2d] = []
        self.limit_vertex = limit_vertex

    @property
    def vec(self):
        return self.plane.parent_vector

    def rotate(self, angle):
        for vertex in self.vertices:
            vertex.rotate(angle)

    def scale(self, factor):
        lengths = [vertex.length() for vertex in self.vertices]
        if factor > 1:
            if max(lengths) * factor <= self.vertices[0].max_length or \
                    not self.limit_vertex:
                for vertex in self.vertices:
                    vertex.scale(factor)
        elif factor < 1:
            if min(lengths) * factor >= 1:
                for vertex in self.vertices:
                    vertex.scale(factor)

    def show(self, window, color=BLACK, width=1, show_vertex=False, aa=False):
        if show_vertex:
            # self.position_vec.show(window)
            for vertex in self.vertices:
                vertex.show(window, color=color, width=width, aa=aa)
        if aa:
            pg.draw.aalines(window, color, True,
                            [vertex.HEAD for vertex in self.vertices], width)
        else:
            pg.draw.lines(window, color, True,
                          [vertex.HEAD for vertex in self.vertices], width)


class rectangle(shape):

    def __init__(self,
                 parent_space: CartesianPlane,
                 size: tuple,
                 limit_vertex=True) -> None:
        super().__init__(parent_space, limit_vertex)

        length = sqrt((size[0]//2)**2 + (size[1]//2)**2)

        for i in range(4):
            self.vertices.append(
                Vector2d(self.plane, length, 0, max_length=self.plane.x_max))
            self.vertices[-1].rotate(pi/2 + pi/2 * i)


class triangle(shape):

    def __init__(self,
                 parent_space: CartesianPlane,
                 size: tuple,
                 limit_vertex=True) -> None:
        super().__init__(parent_space, limit_vertex)

        for i in range(3):
            self.vertices.append(
                Vector2d(self.plane, size[i], 0, max_length=self.plane.x_max))
            self.vertices[-1].rotate(pi/2 + 2*pi/3 * i)


class polygon(shape):

    def __init__(self,
                 parent_space: CartesianPlane,
                 vertex_count: int = 2,
                 size: float = 1.0,
                 limit_vertex: bool = True) -> None:
        super(polygon, self).__init__(parent_space, limit_vertex)

        if vertex_count < 2:
            raise ValueError("Wrong vertex_count, The minimum is 2")

        for i in range(vertex_count):
            self.vertices.append(
                Vector2d(self.plane, size, 0, max_length=self.plane.x_max))
            self.vertices[-1].rotate(pi/2 + 2*pi/vertex_count * i)
