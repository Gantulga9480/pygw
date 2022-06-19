from Game import Game
from Game.graphic import CartesianPlane, Polygon
from Game.physics import (object_body, FreeBody, DynamicBody, StaticPolygonBody)
from Game.physics import Engine
from Game.math import LSI
import pygame as pg
import numpy as np


class Ray(FreeBody):

    def __init__(self, body_id: int, plane: CartesianPlane) -> None:
        super().__init__(body_id, plane, 2)
        self.shape = Polygon(plane, (50, 0))
        self.radius = 50

    def USR_resolve_collision(self, o: object_body, dxy: tuple) -> None:
        # super().USR_resolve_collision(o, dxy)
        for i in range(1):
            if self.collision_point[i].x != 0 or self.collision_point[i].y != 0:
                xy = self.shape.plane.to_XY((self.collision_point[i].x, self.collision_point[i].y))
                pg.draw.circle(self.shape.window, (255, 0, 0), xy, 5)
                print(np.sqrt(self.collision_point[i].x**2 + self.collision_point[i].y**2))


class Test(Game):

    def __init__(self) -> None:
        super().__init__(width=1920, height=1080, flags=pg.FULLSCREEN | pg.HWSURFACE)
        self.plane = CartesianPlane(self.window, (self.width, self.height))
        self.r = Ray(0, self.plane.createPlane(200, 200))
        self.s = StaticPolygonBody(1, self.plane.createPlane(), (100, 100, 100, 100))

        self.e = Engine(self.plane, np.array([self.r, self.s], dtype=object_body))

        self.mainloop()

    def USR_eventHandler(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_q:
                self.running = False

    def USR_loop(self):
        if self.keys[pg.K_UP]:
            self.r.Accelerate(0.5)
        elif self.keys[pg.K_DOWN]:
            self.r.Accelerate(-0.5)
        if self.keys[pg.K_LEFT]:
            self.r.rotate(0.1)
        elif self.keys[pg.K_RIGHT]:
            self.r.rotate(-0.1)

        if self.keys[pg.K_w]:
            self.r.Accelerate(0.5)
        elif self.keys[pg.K_s]:
            self.r.Accelerate(-0.5)

    def USR_render(self):
        self.e.update()
        # self.r.step()
        # self.r.show((255, 0, 0))
        # self.s.show((0, 0, 0))


Test()
