from pygw import Game, Window
from pygw.graphic import CartesianPlane, Triangle
from math import pi
import pygame as core


class RotatingTriangle(Game):

    def __init__(self):
        super().__init__()
        self.angular_velocity = pi / 2

    def setup(self):
        self.add_window(Window(self, self.title))
        self.shape = Triangle(CartesianPlane(self.display_surface, self.size), (70,) * 3)

    def loop(self):
        self.shape.rotate(self.angular_velocity / self.fps)
        self.shape.sync()

    def on_event(self, event):
        if event.type == core.KEYDOWN:
            if event.key == core.K_UP:
                self.angular_velocity += pi / 10
            elif event.key == core.K_DOWN:
                self.angular_velocity -= pi / 10

    def on_render(self):
        self.window.surface.fill((255, 255, 255))
        self.shape.show()


if __name__ == "__main__":
    RotatingTriangle().loop_forever()
