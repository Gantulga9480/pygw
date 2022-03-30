from Game import Game, BLACK
from Game import Plane, Vector
import pygame as pg


class test(Game):

    def __init__(self,
                 title: str = 'PyGameDemo',
                 width: int = 640,
                 height: int = 480,
                 fps: int = 60,
                 render: bool = True) -> None:
        super().__init__(title, width, height, fps, render)
        self.p = Plane((width,  height), mode='center')
        self.v = Vector(2, 2, self.p)

    def USR_render(self):
        pg.draw.circle(self.game_window, BLACK, self.p.center, 10)
        


p = Plane((640, 480), mode='center')
v = Vector(1, 0, p)

print(v.direction)
print(v.length)
