from Game import Game
from Game.graphic import CartesianPlane, Polygon
from Game.physics import (object_body,
                          FreeBody,
                          DynamicBody,
                          StaticPolygonBody,
                          DynamicPolygonBody,
                          Ray)
from Game.physics import Engine
import pygame as pg
import numpy as np


class Sensor:

    def __init__(self, id: int, plane: CartesianPlane, vertex_count: int, radius: float) -> None:
        self.rays: list[Ray] = []
        for i in range(vertex_count):
            self.rays.append(Ray(id, plane, radius))
            self.rays[-1].shape.vertices[0].rotate(np.pi/2 + 2*np.pi/vertex_count * i)

    def reset(self):
        for ray in self.rays:
            ray.reset()


class Test(Game):

    def __init__(self) -> None:
        super().__init__(width=1920, height=1080, flags=pg.FULLSCREEN | pg.HWSURFACE)
        self.plane = CartesianPlane(self.window, (self.width, self.height))

        self.r = Sensor(0, self.plane.createPlane(), 6, 100)

        self.d = DynamicPolygonBody(0, self.plane.createPlane(200, 200), (30, 30, 30), 5)

        for r in self.r.rays:
            self.d.attach(r, True)

        self.s = StaticPolygonBody(1, self.plane.createPlane(), (30, 30, 30, 30))

        self.s1 = StaticPolygonBody(1, self.plane.createPlane(200, 0), (30, 30, 30, 30))

        b = []
        b.append(self.d)
        b.append(self.s)
        b.append(self.s1)
        b.extend(self.r.rays)

        self.e = Engine(self.plane, np.array(b, dtype=object_body))

        self.mainloop()

    def USR_eventHandler(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_q:
                self.running = False

    def USR_loop(self):
        if self.keys[pg.K_UP]:
            self.d.Accelerate(0.5)
        elif self.keys[pg.K_DOWN]:
            self.d.Accelerate(-0.5)
        if self.keys[pg.K_LEFT]:
            self.d.rotate(0.1)
        elif self.keys[pg.K_RIGHT]:
            self.d.rotate(-0.1)

    def USR_render(self):
        self.r.reset()
        self.e.update()


Test()
