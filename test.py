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

        for i in range(100):
            vec = self.plane.createRandomVector()
            if i % 2:
                body_lst.append(
                        TriangleBody(i,
                                     1,
                                     CartesianPlane(self.window, (100, 100), vec),
                                     (20, 20, 20)))
            else:
                body_lst.append(
                        RectBody(i,
                                 1,
                                 CartesianPlane(self.window, (100, 100), vec),
                                 (20*math.sqrt(2), 20*math.sqrt(2))))
            rot = random.random()*6 - 3
            body_lst[-1].rotate(rot)

        y = 540
        for i in range(28):
            vec = self.plane.createVector(-960, y)
            body_lst.append(RectBody(1,
                                     0,
                                     CartesianPlane(self.window, (900, 900), vec),
                                     (40, 40)))
            vec = self.plane.createVector(960, y)
            body_lst.append(RectBody(1,
                                     0,
                                     CartesianPlane(self.window, (900, 900), vec),
                                     (40, 40)))
            y -= 40

        x = -920
        for i in range(47):
            vec = self.plane.createVector(x, 540)
            body_lst.append(RectBody(1,
                                     0,
                                     CartesianPlane(self.window, (900, 900), vec),
                                     (40, 40)))
            vec = self.plane.createVector(x, -540)
            body_lst.append(RectBody(1,
                                     0,
                                     CartesianPlane(self.window, (900, 900), vec),
                                     (40, 40)))
            x += 40

        vec = self.plane.createVector(100, 0)
        body_lst.append(PolygonBody(1,
                                    1,
                                    CartesianPlane(self.window, (900, 900), vec),
                                    (30, 30, 30, 30, 30)))

        self.bodies = np.array(body_lst, dtype=object_body)
        self.engine = Engine(self.plane, self.bodies)

    def USR_loop(self):
        if self.keys[pg.K_UP]:
            self.bodies[-1].accelerate(0.1)
            # self.test_body_vec.y += 1
        elif self.keys[pg.K_DOWN]:
            self.bodies[-1].stop(1.1)
            # self.test_body_vec.y -= 1
        if self.keys[pg.K_LEFT]:
            self.bodies[-1].rotate(0.06)
            # self.test_body_vec.x -= 1
        elif self.keys[pg.K_RIGHT]:
            self.bodies[-1].rotate(-0.06)
            # self.test_body_vec.x += 1

    def USR_render(self):
        self.bodies[-1].step()
        self.engine.step()
        self.set_title(f'fps {round(self.clock.get_fps())}')


Test().mainloop()
