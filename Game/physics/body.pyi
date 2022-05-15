from Game.graphic.cartesian import CartesianPlane, Vector2d
from Game.graphic.shapes import polygon


STATIC = 0
DYNAMIC = 1


class body:
    def __init__(self, state: int, radius: float) -> None: ...


class static_body(body):
    def __init__(self, radius: float) -> None: ...


class dynamic_body(body):
    def __init__(self, space: CartesianPlane, radius: float) -> None: ...
    def react(self, body: dynamic_body, pos: Vector2d, factor: float): ...


class base_body(polygon):
    def __init__(self, body_type: int, pos: Vector2d, vertex_count: int = 2, size: float = 1, limit_vertex: bool = True) -> None: ...
