from Game import *
from Game.graphic import *
from Game.math import *
from Game.physics import *
import numpy as np
import pygame as pg


class Environment(Game):

    def __init__(self,
                 title: str = 'ENV',
                 width: int = 1920,
                 height: int = 1080,
                 fps: int = 60,
                 flags: int = pg.FULLSCREEN | pg.HWSURFACE,
                 render: bool = True) -> None:
        super().__init__(title, width, height, fps, flags, render)

        self.plane = CartesianPlane(self.window, (width, height), 1, None)

        self.shape_vec = self.plane.createVector(1, 0)

        self.shape_plane = CartesianPlane(self.window, (500, 500), 1, self.shape_vec)

        self.rec = triangle(self.shape_plane, (100, 100, 30))

    def USR_eventHandler(self, event):
        ...

    def USR_loop(self):
        self.shape_vec.x = self.plane.to_x(self.mouse_x)
        self.shape_vec.y = self.plane.to_y(self.mouse_y)

        if self.keys[pg.K_UP]:
            self.rec.scale(1.1)
        elif self.keys[pg.K_DOWN]:
            self.rec.scale(1/1.1)
        if self.keys[pg.K_LEFT]:
            self.rec.rotate(0.05)
        elif self.keys[pg.K_RIGHT]:
            self.rec.rotate(-0.05)

    def USR_render(self):
        self.plane.show()
        self.shape_plane.show()
        self.rec.show(RED, True)


Environment().mainloop()
