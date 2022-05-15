from Game.base import Game
from Game.graphic.cartesian import CartesianPlane, Vector2d
from Game.physics.body import *
from Game.physics.collision import collision_detector
from Game.physics.engine import Engine
from Game.color import BLACK, RED, GREEN, BLUE, WHITE
import pygame as pg
import random
import numpy as np


FPS = 60


class Test(Game):

    def __init__(self, title: str = 'PyGameDemo',
                 width: int = 1920, height: int = 1080,
                 fps: int = FPS, render: bool = True) -> None:
        super().__init__(title, width, height, fps, render)

        self.plane = CartesianPlane((width, height), 1)
        self.collider = collision_detector(self.plane)

        self.num_shapes = 100

        body_lst = []

        for i in range(self.num_shapes):
            body_lst.append(
                base_body(
                    i,
                    1,
                    self.plane.createRandomVector(set_limit=True),
                    3, 20))
            rot = random.random()*6 - 3
            body_lst[-1].rotate(rot)
        self.bodies = np.array(body_lst, dtype=base_body)
        self.engine = Engine(self.plane, self.bodies)

    def USR_eventHandler(self, event):
        ...

    def USR_loop(self):
        if self.keys[pg.K_UP]:
            self.bodies[0].accel(1)
        elif self.keys[pg.K_DOWN]:
            self.bodies[0].stop(1/1.1)
        if self.keys[pg.K_LEFT]:
            self.bodies[0].rotate(6)
        elif self.keys[pg.K_RIGHT]:
            self.bodies[0].rotate(-6)
        self.engine.step()

    def USR_render(self):
        for i in range(len(self.bodies)):
            # if random.random() > 0.5:
            #     self.bodies[i].accel(1)
            # else:
            #     self.bodies[i].stop(1/1.1)
            # if random.random() > 0.5:
            #     self.bodies[i].rotate(6)
            # else:
            #     self.bodies[i].rotate(-6)
            self.bodies[i].show(self.window, BLACK, 1, show_vertex=False)
        self.set_title(f'fps {round(self.clock.get_fps())}')


Test().mainloop()
