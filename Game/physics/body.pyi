from Game.graphic.cartesian import CartesianPlane, Vector2d
from Game.graphic.shapes import polygon, polygon_test
from pygame.color import Color
from pygame import Surface


STATIC: int
DYNAMIC: int


class body_dynamics:

    def __init__(self, space: CartesianPlane, radius: float) -> None: ...

    def react(self, pos: Vector2d): ...


class base_body(polygon):

    def __init__(self,
                 id: int,
                 body_type: int,
                 plane: CartesianPlane,
                 vertex_count: int = 2,
                 size: float = 1) -> None: ...

    def step(self) -> None: ...

    def accel(self, factor: float) -> None: ...

    def stop(self, factor: float) -> None: ...

    def rotate(self, angle: float) -> None: ...

    def show(self,
             color: Color,
             show_vertex: bool = False) -> None: ...


class base_body_test(polygon_test):

    def __init__(self,
                 id: int,
                 body_type: int,
                 plane: CartesianPlane,
                 sizes: list) -> None: ...

    def step(self) -> None: ...

    def accel(self, factor: float) -> None: ...

    def stop(self, factor: float) -> None: ...

    def rotate(self, angle: float) -> None: ...

    def show(self,
             color: Color,
             show_vertex: bool = False) -> None: ...
