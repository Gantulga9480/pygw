from Game.base import Game
from Game.graphic.cartesian import CartesianPlane, Vector2d
from Game.graphic.shapes import triangle, rectangle, polygon, shape
from Game.physics.body import *
from Game.physics.collision import LineIntersectCollision as LIC
from Game.color import BLACK, RED, GREEN, BLUE, WHITE
import pygame as pg
import random


FPS = 60


def my_collision(b1: base_body, b2: base_body, d: list):
    scale = 0.9
    if b1.body.state == DYNAMIC and b2.body.state == STATIC:
        b1.body.velocity.scale(scale)
        b1.body.acceleration.scale(scale)
        b1.vec.x -= d[0]
        b1.vec.y -= d[1]
    elif b1.body.state == STATIC and b2.body.state == DYNAMIC:
        b2.body.velocity.scale(scale)
        b2.body.acceleration.scale(scale)
        b2.vec.x += d[0]
        b2.vec.y += d[1]
    elif b1.body.state == DYNAMIC and b2.body.state == DYNAMIC:
        b1.body.velocity.scale(scale)
        b2.body.velocity.scale(scale)
        b1.body.acceleration.scale(scale)
        b2.body.acceleration.scale(scale)
        b1.vec.x -= d[0]/2
        b1.vec.y -= d[1]/2
        b2.vec.x += d[0]/2
        b2.vec.y += d[1]/2


def my_dynamic(body: dynamic_body, pos: Vector2d, factor):
    a_len = body.acceleration.length()
    if round(a_len, 2) > 1:
        body.velocity.x += body.acceleration._head.x.value
        body.velocity.y += body.acceleration._head.y.value
        body.acceleration.scale(1/1.1)
    else:
        body.acceleration.head = body.acceleration.unit(vector=False)
    v_len = body.velocity.length()
    if round(v_len, 2) > 1:
        pos.x += body.velocity._head.x.value / factor
        pos.y += body.velocity._head.y.value / factor
        body.velocity.sub(v_len * 0.01)
    else:
        body.velocity.head = body.velocity.unit(vector=False)


class TestBody(base_body):

    def __init__(self,
                 body_id,
                 body_type,
                 pos: Vector2d,
                 vertex_count: int = 2,
                 size: float = 1,
                 limit_vertex: bool = True) -> None:
        super().__init__(body_type,
                         pos,
                         vertex_count,
                         size,
                         limit_vertex,
                         my_dynamic)
        self.id = body_id

    def rotate(self, angle):
        a = angle/FPS
        super().rotate(a)
        self.body.acceleration.rotate(a)
        self.body.velocity.rotate(a)

    def step(self):
        if self.body.state == DYNAMIC:
            self.body.step(self.plane.parent_vector, FPS)


class Test(Game):

    def __init__(self, title: str = 'PyGameDemo',
                 width: int = 1600, height: int = 800,
                 fps: int = FPS, render: bool = True) -> None:
        super().__init__(title, width, height, fps, render)

        self.plane = CartesianPlane((width, height), 1)
        self.collider = LIC(self.plane, my_collision)

        self.bodies: list[TestBody] = []

        self.selected = 0
        self.num_shapes = 100

        self.bodies.append(
            TestBody(
                0,
                DYNAMIC, self.plane.createRandomVector(set_limit=True), 3, 20))

        for i in range(self.num_shapes):
            self.bodies.append(
                TestBody(
                    i+1,
                    DYNAMIC,
                    self.plane.createRandomVector(set_limit=True),
                    random.randint(3, 7), 10))
            rot = random.random()*6 - 3
            self.bodies[-1].rotate(rot)

    def USR_eventHandler(self):
        for event in self.events:
            if event.type == pg.KEYUP:
                if event.key == pg.K_q:
                    if self.selected > 0:
                        self.selected -= 1
                elif event.key == pg.K_e:
                    if self.selected < self.num_shapes - 1:
                        self.selected += 1
        if self.keys[pg.K_UP]:
            self.bodies[self.selected].body.acceleration.add(1)
        elif self.keys[pg.K_DOWN]:
            self.bodies[self.selected].body.velocity.scale(1/1.1)
        if self.keys[pg.K_LEFT]:
            self.bodies[self.selected].rotate(6)
        elif self.keys[pg.K_RIGHT]:
            self.bodies[self.selected].rotate(-6)

    def USR_loop(self):
        for b in self.bodies:
            if b.id == 0:
                b.step()
                continue
            if random.random() > 0.5:
                b.body.acceleration.add(1)
            else:
                b.body.acceleration.scale(1/1.1)
            if random.random() > 0.5:
                b.rotate(6)
            else:
                b.rotate(-6)
            b.step()

    def USR_render(self):
        for i in self.bodies:
            for j in self.bodies:
                if i is not j:
                    if i.body.state is not STATIC or \
                            j.body.state is not STATIC:
                        if (i.body.radius + j.body.radius) >= \
                                i.vec.distance_to(j.vec):
                            p = self.collider.dynamic_collision(i, j)
                            if p:
                                for point in p:
                                    pg.draw.circle(self.window,
                                                   RED, point, 5)

            i.show(self.window, show_vertex=False, aa=True)
            # i.body.velocity.show(self.window, color=GREEN)
            i.body.acceleration.show(self.window, width=3, color=BLUE)

    def USR_loopEnd(self):
        self.set_title(f'fps {round(self.clock.get_fps())}')


Test().mainloop()
