from Game.base import Game
from Game.graphic import CartesianPlane
from Game.physics import base_body, base_body_test
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
                                    unit_length=0.5)
        body_lst = []

        for i in range(100):
            vec = self.plane.createRandomVector()
            body_lst.append(
                base_body_test(i,
                               1,
                               CartesianPlane(self.window, (10, 10), vec),
                               [100, 1, 100, 100, 100]))
            rot = random.random()*6 - 3
            body_lst[-1].rotate(rot)

        # for i in range(50):
        #     body_lst.append(
        #         base_body(i,
        #                   1,
        #                   self.plane.createVector(i*20 - width/4,
        #                                           400, set_limit=True),
        #                   vertex_count=5,
        #                   size=10))
        #     rot = random.random()*6 - 3
        #     body_lst[-1].rotate(rot)

        # for i in range(50):
        #     body_lst.append(
        #         base_body(i,
        #                   1,
        #                   self.plane.createVector(i*20 - width/4,
        #                                           -400, set_limit=True),
        #                   vertex_count=5,
        #                   size=10))
        #     rot = random.random()*6 - 3
        #     body_lst[-1].rotate(rot)

        # body_lst.append(
        #     base_body(1000+i,
        #               0,
        #               self.plane.createVector(-400, 0, set_limit=True),
        #               vertex_count=4,
        #               size=200))
        # body_lst[-1].rotate(math.pi/4)

        self.test_body_vec = self.plane.createVector(400, 0, max_length=200)

        body_lst.append(
            base_body_test(1000+i,
                           1,
                           CartesianPlane(self.window, (100, 100),
                                          self.test_body_vec),
                           [100, 1, 100, 100, 100]))
        body_lst[-1].rotate(math.pi/4)

        self.bodies = np.array(body_lst, dtype=base_body)
        self.engine = Engine(self.plane, self.bodies)

    def USR_loop(self):
        # self.test_body_vec.x = self.plane.to_x(self.mouse_x)
        # self.test_body_vec.y = self.plane.to_y(self.mouse_y)
        if self.keys[pg.K_UP]:
            self.bodies[-1].accel(10)
            # self.test_body_vec.y += 1
        elif self.keys[pg.K_DOWN]:
            self.bodies[-1].stop(1.1)
            # self.test_body_vec.y -= 1
        if self.keys[pg.K_LEFT]:
            self.bodies[-1].rotate(0.01)
            # self.test_body_vec.x -= 1
        elif self.keys[pg.K_RIGHT]:
            self.bodies[-1].rotate(-0.01)
            # self.test_body_vec.x += 1

    def USR_render(self):
        self.bodies[-1].step()
        self.engine.step()
        self.set_title(f'fps {round(self.clock.get_fps())}')


Test().mainloop()
