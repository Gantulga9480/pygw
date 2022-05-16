from Game.graphic.cartesian import CartesianPlane


class Engine:

    def __init__(self, plane: CartesianPlane, bodies: memoryview) -> None: ...
    def step(self) -> None: ...
