from Game.base import Game
from Game.graphic.cartesian import CartesianPlane, Vector2d
import pygame as pg


class game(Game):

    def __init__(self,
                 title: str = 'PyGameDemo',
                 width: int = 640,
                 height: int = 480,
                 fps: int = 60,
                 render: bool = True) -> None:
        super().__init__(title, width, height, fps, render)

        self.plane = CartesianPlane((width, height), 1)
        self.vec = Vector2d(self.plane, max_length=100, min_length=1)

    def USR_eventHandler(self):
        if self.keys[pg.K_UP]:
            self.vec.scale(1.1)
        elif self.keys[pg.K_DOWN]:
            self.vec.scale(1/1.1)

        if self.keys[pg.K_LEFT]:
            self.vec.rotate(0.1)
        elif self.keys[pg.K_RIGHT]:
            self.vec.rotate(-0.1)

    def USR_render(self):
        self.vec.show(self.window)


game().mainloop()
