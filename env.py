from Game.base import Game
from Game.graphic import CartesianPlane
from Game.physics import (object_body,
                          DynamicPolygonBody,
                          StaticPolygonBody,
                          StaticRectangleBody,
                          FreePolygonBody,
                          Ray)
from Game.physics import Engine
import pygame as pg
import numpy as np
import json
from math import dist


class Sensor:

    def __init__(self,
                 id: int,
                 plane: CartesianPlane,
                 ray_count: int,
                 radius: float) -> None:
        self.rays: list[Ray] = []
        for i in range(ray_count):
            r = Ray(id, plane, radius)
            r.shape.color = (230, 230, 230)
            r.shape.vertices[0].rotate(np.pi/2 + 2*np.pi/ray_count * i)
            self.rays.append(r)

    def state(self):
        s = []
        for ray in self.rays:
            d = dist([ray.x, ray.y], [0, 0])
            if d == 0:
                s.append(ray.radius)
            else:
                s.append(d)
        return s

    def reset(self):
        for ray in self.rays:
            ray.reset()


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
                StaticRectangleBody(0,
                                    CartesianPlane(self.window, (40, 40), vec),
                                    (40, 40)))
            vec = self.plane.createVector(width/2, y)
            self.bodies.append(
                StaticRectangleBody(0,
                                    CartesianPlane(self.window, (40, 40), vec),
                                    (40, 40)))
            y -= 40

        x = -width/2 + 40
        for _ in range(47):
            vec = self.plane.createVector(x, height / 2)
            self.bodies.append(
                StaticRectangleBody(0,
                                    CartesianPlane(self.window, (40, 40), vec),
                                    (40, 40)))
            vec = self.plane.createVector(x, -height / 2)
            self.bodies.append(
                StaticRectangleBody(0,
                                    CartesianPlane(self.window, (40, 40), vec),
                                    (40, 40)))
            x += 40

        a = dict()

        with open('objects.json') as f:
            a = json.load(f)

        for body in a['bodies']:
            vec = self.plane.createVector(body['x'], body['y'])
            size = tuple([body['size'] for _ in range(body['shape'])])
            if body['type'] == 1:
                p = DynamicPolygonBody(1,
                                       CartesianPlane(self.window,
                                                      (40, 40), vec), size, 10)
                p.shape.color = (255, 0, 255)
            else:
                p = StaticPolygonBody(0,
                                      CartesianPlane(self.window,
                                                     (40, 40), vec), size)
            p.rotate(body['dir'])
            self.bodies.append(p)

        self.agent: DynamicPolygonBody = self.bodies[-1]
        self.r = Sensor(1, self.plane.createPlane(), 10, 100)
        a = FreePolygonBody(1, self.plane.createPlane(), (17, 5, 5))
        a.shape.color = (0, 0, 255)
        self.agent.attach(a, True)
        for r in self.r.rays:
            self.agent.attach(r, True)

        self.bodies.extend(self.r.rays)
        self.bodies.append(a)

        self.engine = Engine(self.plane, np.array(self.bodies,
                                                  dtype=object_body))

    def USR_eventHandler(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                self.running = False

    def USR_loop(self):
        if self.keys[pg.K_UP]:
            self.agent.Accelerate(0.2)
        elif self.keys[pg.K_DOWN]:
            self.agent.Accelerate(-0.2)
        if self.keys[pg.K_LEFT]:
            self.agent.rotate(0.06)
        elif self.keys[pg.K_RIGHT]:
            self.agent.rotate(-0.06)

    def USR_render(self):
        self.r.reset()
        self.engine.update()
        print(f'v: {self.agent.speed()}, d: {self.agent.direction()}')
        print(self.r.state())


env = Environment()

while env.running:
    env.loop_once()
