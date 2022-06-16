from Game import Game
from Game.graphic import CartesianPlane, Polygon
from Game.physics import (object_body, FreeBody, DynamicBody, StaticPolygonBody)
from Game.physics import Engine
from Game.math import LSI
import pygame as pg
import numpy as np


class Ray(FreeBody):

    def __init__(self, body_id: int, plane: CartesianPlane) -> None:
        super().__init__(body_id, plane)
        self.shape = Polygon(plane, (50, 0))
        self.radius = 50

    def USR_resolve_collision(self, o: object_body, dxy: tuple) -> None:
        for i in range(1):
            # check for every vertex of first shape against ...
            l1s = self.shape.plane.get_parent_vector().plane.to_xy(self.shape.vertices[i].TAIL)
            l1e = self.shape.plane.get_parent_vector().plane.to_xy(self.shape.vertices[i].HEAD)
            xy = self.shape.plane.get_parent_vector().plane.to_XY(l1e)
            pg.draw.circle(self.shape.plane.window, (255, 0, 0), xy, 5)
            xy = self.shape.plane.get_parent_vector().plane.to_XY(l1s)
            pg.draw.circle(self.shape.plane.window, (255, 0, 0), xy, 5)
            for j in range(o.shape.vertex_count):
                # ... every edge of second shape
                l2s = self.shape.plane.get_parent_vector().plane.to_xy(o.shape.vertices[j].HEAD)
                l2e = self.shape.plane.get_parent_vector().plane.to_xy(o.shape.vertices[(j+1)%o.shape.vertex_count].HEAD)
                # check these two line segments are intersecting or not
                val = LSI(l1s[0], l1s[1], l1e[0], l1e[1], l2s[0], l2s[1], l2e[0], l2e[1])
                if val != 0:
                    x = self.shape.plane.to_X((l1e[0] - l1s[0]) * val)
                    y = self.shape.plane.to_Y((l1e[1] - l1s[1]) * val)
                    pg.draw.circle(self.shape.plane.window, (255, 0, 0), (x, y), 5)


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
        self.e.step()
        # self.r.step()
        # self.r.show((255, 0, 0))
        # self.s.show((0, 0, 0))


Test()
