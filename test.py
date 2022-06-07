from Game.base import Game
from Game.graphic import CartesianPlane
from Game.physics import PolygonBody, TriangleBody, RectBody
from Game.physics.body import object_body
from Game.physics import Engine
import numpy as np
import pygame as pg
import random
import math


class Test(Game):

    def __init__(self,
                 title: str = 'PyGameDemo',
                 width: int = 1920,
                 height: int = 1080,
                 fps: int = 60,
                 flags: int = pg.FULLSCREEN | pg.HWSURFACE,
                 render: bool = True) -> None:
        super().__init__(title, width, height, fps, flags, render)

        self.plane = CartesianPlane(self.window, (width, height),
                                    unit_length=1)
        body_lst = []

        for i in range(500):
            vec = self.plane.createRandomVector()
            if i % 2:
                body_lst.append(
                        PolygonBody(i,
                                    1,
                                    CartesianPlane(self.window, (20, 20), vec),
                                    (10, 10, 10, 10, 10)))
            else:
                body_lst.append(
                        RectBody(i,
                                 1,
                                 CartesianPlane(self.window, (20, 20), vec),
                                 (10*math.sqrt(2), 10*math.sqrt(2))))
            rot = random.random()*6 - 3
            body_lst[-1].rotate(rot)

        y = height / 2
        for i in range(28):
            vec = self.plane.createVector(-width/2, y)
            body_lst.append(
                RectBody(1, 0, CartesianPlane(self.window, (40, 40), vec),
                         (40, 40)))
            vec = self.plane.createVector(width/2, y)
            body_lst.append(
                RectBody(1, 0, CartesianPlane(self.window, (40, 40), vec),
                         (40, 40)))
            y -= 40

        x = -width/2 + 40
        for i in range(47):
            vec = self.plane.createVector(x, height / 2)
            body_lst.append(
                RectBody(1, 0, CartesianPlane(self.window, (40, 40), vec),
                         (40, 40)))
            vec = self.plane.createVector(x, -height / 2)
            body_lst.append(
                RectBody(1, 0, CartesianPlane(self.window, (40, 40), vec),
                         (40, 40)))
            x += 40

        vec = self.plane.createVector(100, 0)
        body_lst.append(PolygonBody(1,
                                    1,
                                    CartesianPlane(self.window, (40, 40), vec),
                                    (20, 20, 20, 20, 20)))

        self.bodies = np.array(body_lst, dtype=object_body)
        self.engine = Engine(self.plane, self.bodies)

    def USR_loop(self):
        if self.keys[pg.K_UP]:
            self.bodies[-1].accelerate(0.1)
        elif self.keys[pg.K_DOWN]:
            self.bodies[-1].stop(1.1)
        if self.keys[pg.K_LEFT]:
            self.bodies[-1].rotate(0.06)
        elif self.keys[pg.K_RIGHT]:
            self.bodies[-1].rotate(-0.06)

    def USR_render(self):
        self.bodies[-1].step()
        self.engine.step()
        self.set_title(f'fps {round(self.clock.get_fps())}')


Test().mainloop()
