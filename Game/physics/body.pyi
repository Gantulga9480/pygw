from Game.graphic.cartesian import CartesianPlane, Vector2d
from Game.graphic.shapes import Shape


class object_body:
    type: int
    id: int
    radius: float
    friction_coef: float
    drag_coef: float
    shape: Shape
    velocity: Vector2d
    def __init__(self, id: int, type: int) -> None: ...
    def position(self) -> tuple: ...
    def direction(self) -> None: ...
    def speed(self) -> float: ...
    def step(self) -> None: ...
    def USR_step(self) -> None: ...
    def USR_resolve_collision(self, o: object_body, dxy: tuple) -> None: ...
    def USR_resolve_collision_point(self, dx: float, dy: float) -> None: ...
    def attach(self, o: object_body, follow_dir: bool) -> None: ...
    def detach(self) -> None: ...
    def rotate(self, angle: float) -> None: ...
    def scale(self, factor: float) -> None: ...
    def show(self, vertex: bool = False, velocity: bool = False) -> None: ...


class FreeBody(object_body):
    def __init__(self, id: int, plane: CartesianPlane, max_speed: float = 0, drag_coef: float = 0) -> None: ...
    def accelerate(self, factor: float) -> None: ...


class StaticBody(object_body):
    def __init__(self, id: int, plane: CartesianPlane) -> None: ...


class DynamicBody(object_body):
    def __init__(self, id: int, plane: CartesianPlane, max_speed: float = 1, drag_coef: float = 0.03, friction_coef: float = 0.3) -> None: ...
    def accelerate(self, factor: float) -> None: ...


class DynamicPolygonBody(DynamicBody):
    def __init__(self, id: int, plane: CartesianPlane, size: tuple, max_speed: float = 1, drag_coef: float = 0.03, friction_coef: float = 0.3) -> None: ...


class DynamicRectangleBody(DynamicBody):
    def __init__(self, id: int, plane: CartesianPlane, size: tuple, max_speed: float = 1, drag_coef: float = 0.03, friction_coef: float = 0.3) -> None: ...


class DynamicTriangleBody(DynamicBody):
    def __init__(self, id: int, plane: CartesianPlane, size: tuple, max_speed: float = 1, drag_coef: float = 0.03, friction_coef: float = 0.3) -> None: ...


class StaticPolygonBody(StaticBody):
    def __init__(self, id: int, plane: CartesianPlane, size: tuple) -> None: ...


class StaticRectangleBody(StaticBody):
    def __init__(self, id: int, plane: CartesianPlane, size: tuple) -> None: ...


class StaticTriangleBody(StaticBody):
    def __init__(self, id: int, plane: CartesianPlane, size: tuple) -> None: ...


class FreePolygonBody(FreeBody):
    def __init__(self, id: int, plane: CartesianPlane, size: tuple, max_speed: float = 0, drag_coef: float = 0) -> None: ...


class Ray(FreeBody):
    x: float
    y: float
    def __init__(self, id: int, plane: CartesianPlane, length: float, max_speed: float = 0, drag_coef: float = 0) -> None: ...
    def reset(self) -> None: ...
