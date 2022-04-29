from Game.graphic.cartesian import CartesianPlane, Vector2d
from Game.graphic.shapes import shape, polygon, rectangle, triangle

STATIC = 0
DYNAMIC = 1


class body:

    def __init__(self) -> None:
        self.acceleration = None


class body(polygon):

    def __init__(self,
                 parent_space: CartesianPlane,
                 positon: tuple,
                 vertex_count: int = 2,
                 size: float = 1,
                 state: int = STATIC,
                 limit_vertex: bool = True) -> None:
        super().__init__(parent_space,
                         positon,
                         vertex_count,
                         size,
                         limit_vertex)

        self.state = state
        self.radius = size + 1
        self.inertia = Vector2d(self.plane, 1, 0, set_limit=True)
        self.inertia.rotate(self.start_angle)

    def step(self, dx=0, dy=0):
        if dx and dy:
            self.position_vec.x += dx
            self.position_vec.y += dy
        else:
            if round(self.inertia.length, 2) > 1:
                self.position_vec.x += self.inertia.head_.x.value - 1
                self.position_vec.y += self.inertia.head_.y.value - 1
                # self.inertia *= 0.99

    def rotate(self, angle):
        self.inertia.rotate(angle)
        for vertex in self.vertices:
            vertex.rotate(angle)
