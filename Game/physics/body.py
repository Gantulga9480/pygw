from Game.graphic.cartesian import CartesianPlane
from Game.graphic.shapes import polygon, shape, Vector2d
from Game.physics.core import vector2d
from math import pi

STATIC = 0
DYNAMIC = 1
FREE = 2


class body:

    def __init__(self, state, radius) -> None:
        super(body, self).__init__()
        self.state = state
        self.radius = radius


class static_body(body):

    def __init__(self, radius) -> None:
        super(static_body, self).__init__(STATIC, radius)


class dynamic_body(body):

    def __init__(self, radius) -> None:
        super(dynamic_body, self).__init__(DYNAMIC, radius)
        self.acceleration = vector2d(0, 0, max_length=100)
        self.speed = vector2d(0, 0)


class base_body(polygon):

    def __init__(self,
                 body_type,
                 pos: Vector2d,
                 vertex_count: int = 2,
                 size: float = 1,
                 limit_vertex: bool = True) -> None:
        super().__init__(parent_space=CartesianPlane((size, size), 1, pos),
                         vertex_count=vertex_count,
                         size=size,
                         limit_vertex=limit_vertex)
        self.body_type = body_type
        if body_type == STATIC:
            self.body = static_body(size)
        elif body_type == DYNAMIC:
            self.body = dynamic_body(size)
