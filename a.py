from Game import Game
from Game.graphic import CartesianPlane
from Game.physics import (DynamicPolygonBody,
                          StaticPolygonBody,
                          StaticBody,
                          object_body)
from Game.graphic import Polygon
import pygame as pg


class Sensor(StaticBody):

    def __init__(self, body_id: int, plane: CartesianPlane) -> None:
        super().__init__(body_id, plane)
        self.shape = Polygon(plane, ())

    def USR_resolve_collision(self, o: object_body, dxy: tuple) -> None:
        ...


class Test(Game):

    def __init__(self) -> None:
        super().__init__(width=1920, height=1080, flags=pg.FULLSCREEN | pg.HWSURFACE)
        self.plane = CartesianPlane(self.window, (self.width, self.height))
        p = self.plane.createPlane()
        self.d = DynamicPolygonBody(1, p, (30, 0), 10)
        self.s = DynamicPolygonBody(0, self.plane.createPlane(y=30), (50, 50, 50, 1, 1, 1, 50, 50), 10)
        self.d.attach(self.s, True)
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

        if self.keys[pg.K_w]:
            self.s.Accelerate(0.5)
        elif self.keys[pg.K_s]:
            self.s.Accelerate(-0.5)
        if self.keys[pg.K_a]:
            self.s.rotate(0.1)
        elif self.keys[pg.K_d]:
            self.s.rotate(-0.1)

        if self.keys[pg.K_z]:
            self.d.attach(self.s, True)
        elif self.keys[pg.K_c]:
            self.d.detach(self.s)

        self.d.step()
        self.s.step()

    def USR_render(self):
        self.d.show((255, 0, 0))
        self.s.show((0, 0, 0))


Test()
