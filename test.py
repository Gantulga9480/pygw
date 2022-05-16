from Game.base import Game
from Game.graphic import CartesianPlane
from Game.physics import base_body
from Game.physics import Engine
import numpy as np
import pygame as pg
import random


class Test(Game):

    def __init__(self,
                 title: str = 'PyGameDemo',
                 width: int = 1920,
                 height: int = 1080,
                 fps: int = 60,
                 flags: int = pg.FULLSCREEN | pg.HWSURFACE,
                 render: bool = True) -> None:
        super().__init__(title, width, height, fps, flags, render)

        self.plane = CartesianPlane((width, height), 1)
        body_lst = []

        for i in range(1000):
            body_lst.append(
                base_body(i,
                          1,
                          self.plane.createRandomVector(set_limit=True),
                          vertex_count=3,
                          size=15))
            rot = random.random()*6 - 3
            body_lst[-1].rotate(rot)
        self.bodies = np.array(body_lst, dtype=base_body)
        self.engine = Engine(self.window, self.plane, self.bodies)

    def USR_loop(self):
        if self.keys[pg.K_UP]:
            self.bodies[0].accel(1)
        elif self.keys[pg.K_DOWN]:
            self.bodies[0].stop(1.1)
        if self.keys[pg.K_LEFT]:
            self.bodies[0].rotate(0.1)
        elif self.keys[pg.K_RIGHT]:
            self.bodies[0].rotate(-0.1)

    def USR_render(self):
        self.engine.step()
        self.set_title(f'fps {round(self.clock.get_fps())}')


Test().mainloop()
