from Game.graphic.cartesian import CartesianPlane, Vector2d
from Game.color import BLACK
from pygame.color import Color
from pygame import Surface
import numpy as np
from typing import Union


class Shape:
    window: Surface
    plane: CartesianPlane
    vertex_count: int
    vertices: np.ndarray[Vector2d]
    def __init__(self, plane: CartesianPlane) -> None: ...
    def rotate(self, angle) -> None: ...
    def scale(self, factor) -> None: ...
    def show(self, color: Union[Color, tuple] = BLACK, show_vertex: bool = False) -> None: ...


class Rectangle(Shape):
    def __init__(self, parent_space: CartesianPlane, size: tuple) -> None: ...


class Triangle(Shape):
    def __init__(self, parent_space: CartesianPlane, size: tuple) -> None: ...


class Polygon(Shape):
    def __init__(self, parent_space: CartesianPlane, size: tuple) -> None: ...
