from Game.graphic.cartesian import CartesianPlane, Vector2d
from Game.graphic.shapes import Polygon
from pygame.color import Color


class object_dynamics:
    def __init__(self, space: CartesianPlane, radius: float) -> None: ...
    def react(self, pos: Vector2d): ...


class object_body:

    def __init__(self,
                 id: int,
                 body_type: int,
                 plane: CartesianPlane) -> None: ...

    def step(self) -> None: ...
    def accelerate(self, factor: float) -> None: ...
    def stop(self, factor: float) -> None: ...
    def rotate(self, angle: float) -> None: ...
    def scale(self, factor: float) -> None: ...

    def show(self,
             color: Color,
             show_vertex: bool = False) -> None: ...


class PolygonBody(object_body):

    def __init__(self,
                 body_id: int,
                 body_type: int,
                 plane: CartesianPlane,
                 size: tuple) -> None: ...


class RectBody(object_body):

    def __init__(self,
                 body_id: int,
                 body_type: int,
                 plane: CartesianPlane,
                 size: tuple) -> None: ...


class TriangleBody(object_body):

    def __init__(self,
                 body_id: int,
                 body_type: int,
                 plane: CartesianPlane,
                 sizes: list) -> None: ...
