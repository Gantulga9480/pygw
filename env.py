from Game.base import Game
from Game.graphic import CartesianPlane
from Game.physics import PolygonBody, RectBody, object_body
from Game.physics import Engine
import pygame as pg
import numpy as np
import json


class Environment(Game):

    def __init__(self,
                 title: str = 'ENV',
                 width: int = 1920,
                 height: int = 1080,
                 fps: int = 60,
                 flags: int = pg.FULLSCREEN | pg.HWSURFACE,
                 render: bool = True) -> None:
        super().__init__(title, width, height, fps, flags, render)

        self.plane = CartesianPlane(self.window, (width, height),
                                    unit_length=1)
        self.bodies: list[object_body] = []

        y = height / 2
        for _ in range(28):
            vec = self.plane.createVector(-width/2, y)
            self.bodies.append(
                RectBody(1, 0, CartesianPlane(self.window, (40, 40), vec),
                         (40, 40)))
            vec = self.plane.createVector(width/2, y)
            self.bodies.append(
                RectBody(1, 0, CartesianPlane(self.window, (40, 40), vec),
                         (40, 40)))
            y -= 40

        x = -width/2 + 40
        for _ in range(47):
            vec = self.plane.createVector(x, height / 2)
            self.bodies.append(
                RectBody(1, 0, CartesianPlane(self.window, (40, 40), vec),
                         (40, 40)))
            vec = self.plane.createVector(x, -height / 2)
            self.bodies.append(
                RectBody(1, 0, CartesianPlane(self.window, (40, 40), vec),
                         (40, 40)))
            x += 40

        a = dict()

        with open('objects.json') as f:
            a = json.load(f)

        for body in a['bodies']:
            vec = self.plane.createVector(body['x'], body['y'])
            size = tuple([body['size'] for _ in range(body['shape'])])
            p = PolygonBody(0, body['type'], CartesianPlane(self.window,
                                                            (40, 40),
                                                            vec), size)
            p.rotate(body['dir'])
            self.bodies.append(p)

        self.agent = self.bodies[-1]

        self.engine = Engine(self.plane, np.array(self.bodies,
                                                  dtype=object_body))

    def USR_eventHandler(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                self.running = False

    def USR_loop(self):
        if self.keys[pg.K_UP]:
            self.agent.accelerate(0.2)
        elif self.keys[pg.K_DOWN]:
            self.agent.stop(1.1)
        if self.keys[pg.K_LEFT]:
            self.agent.rotate(0.06)
        elif self.keys[pg.K_RIGHT]:
            self.agent.rotate(-0.06)

    def USR_render(self):
        self.agent.step()
        self.engine.step()

        print(self.agent.get_speed())
        print(self.agent.get_pos())


Environment().mainloop()
