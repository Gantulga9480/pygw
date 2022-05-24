from Game.graphic.cartesian import CartesianPlane
from pygame.color import Color
from pygame import Surface


class shape:

    def __init__(self, plane: CartesianPlane) -> None: ...

    def rotate(self, angle) -> None: ...

    def scale(self, factor) -> None: ...

    def show(self,
             color: Color,
             show_vertex: bool = False) -> None: ...


class rectangle(shape):

    def __init__(self, parent_space: CartesianPlane, size: tuple) -> None: ...


class triangle(shape):

    def __init__(self, parent_space: CartesianPlane, size: tuple) -> None: ...


class polygon(shape):

    def __init__(self,
                 parent_space: CartesianPlane,
                 vertex_count: int = 2,
                 size: float = 1.0) -> None: ...
