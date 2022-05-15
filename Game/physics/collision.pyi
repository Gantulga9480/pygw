from Game.graphic.cartesian import CartesianPlane
from Game.physics.body import base_body


class collision_detector:
    def __init__(self, plane: CartesianPlane) -> None: ...
    def check(self, b1: base_body, b2: base_body) -> None: ...
