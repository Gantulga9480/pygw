from Game.graphic.cartesian import CartesianPlane, Vector2d
from Game.graphic.shapes import polygon


STATIC: int
DYNAMIC: int


class body_dynamics:
    def __init__(self, space: CartesianPlane, radius: float) -> None: ...
    def react(self, pos: Vector2d): ...


class base_body(polygon):
    def __init__(self,
                 id: int,
                 body_type: int,
                 pos: Vector2d,
                 vertex_count: int = 2,
                 size: float = 1,
                 limit_vertex: bool = True) -> None: ...

    def step(self) -> None: ...
    def accel(self, factor: float) -> None: ...
    def stop(self, factor: float) -> None: ...
    def rotate(self, angle: float) -> None: ...
    def show(self, window, color, width, show_vertex) -> None: ...
