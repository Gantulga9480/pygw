from Game.graphic.cartesian import CartesianPlane
from Game.graphic.shapes import polygon, shape
from Game.physics.core import vector2d
from math import pi

STATIC = 0
DYNAMIC = 1
FREE = 2


class body:

    def __init__(self, state) -> None:
        super(body, self).__init__()
        self.state = state
        self.radius = 0


class static_body(body):

    def __init__(self) -> None:
        super(static_body, self).__init__(STATIC)


class dynamic_body(body):

    def __init__(self) -> None:
        super(dynamic_body, self).__init__()
        self.state = DYNAMIC
        self.acceleration = vector2d(1, 0, max_length=100)
        self.inertia = vector2d(1, 0)
        self.inertia.rotate(pi/2)
