from Game import Game, core
from Game.graphic import CartesianPlane, Triangle
from math import pi


class RotatingTriangle(Game):

    def __init__(self) -> None:
        super().__init__()
        self.angular_velocity = pi / 2

    def setup(self):
        self.shape = Triangle(CartesianPlane(self.window, self.size), (70,) * 3)

    def loop(self):
        self.shape.rotate(self.angular_velocity / self.fps)
        self.shape.sync()

    def onEvent(self, event):
        if event.type == core.KEYUP:
            if event.key == core.K_UP:
                self.angular_velocity += pi / 10
            elif event.key == core.K_DOWN:
                self.angular_velocity -= pi / 10

    def onRender(self):
        self.window.fill((255, 255, 255))
        self.shape.show()


if __name__ == "__main__":
    RotatingTriangle().loop_forever()
