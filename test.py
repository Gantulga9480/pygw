from Game import Game, BLACK, RED, GREEN
from Game.graphic.cartesian import scalar, plane, vector
import pygame as pg
import random
import math


WIDTH = 1500
HEIGHT = 900
FPS = 60


class CartesianPlane(plane):

    def __init__(self,
                 size: tuple,
                 unit_length=1) -> None:
        super().__init__(size, unit_length)

    def move(self, x, y):
        is_hit = False
        if 0 <= self._x_dif + x <= self._size[0]:
            self._x_dif += x
        else:
            is_hit = True
            if x > 0:
                self._x_dif = self._size[0]
            else:
                self._x_dif = 0
        if 0 <= self._y_dif - y <= self._size[1]:
            self._y_dif -= y
        else:
            is_hit = True
            if y > 0:
                self._y_dif = 0
            else:
                self._y_dif = self._size[1]
        return is_hit


class agent:

    def __init__(self, x, y) -> None:
        self.plane = CartesianPlane((WIDTH, HEIGHT))
        self.vector = self.plane.vector(x, y)
        self.rect = None
        self.frame_skip_count = 0
        self.frame_count = 0

    def move(self):
        d = self.vector.length / FPS
        speed_x = round(math.cos(self.vector.direction)) * d
        speed_y = round(math.sin(self.vector.direction)) * d
        if d < 1:
            self.frame_skip_count = round(1 / d)
        else:
            self.frame_skip_count = 0
        self.frame_count += 1
        if self.frame_count >= self.frame_skip_count:
            self.frame_skip_count = 0
            self.plane.move(speed_x, speed_y)

    def get_rect(self):
        self.rect = pg.Rect(self.plane.getX(),
                            self.plane.getY(), 0, 0).inflate(30, 30)
        return self.rect


class environment:

    def __init__(self) -> None:
        self.plane = CartesianPlane((WIDTH, HEIGHT))
        self.agents = []
        for _ in range(3):
            self.agents.append(agent(60, 0))

    def step(self):
        for agent in self.agents:
            if 50 <= agent.vector.length <= WIDTH//4:
                if random.random() > 0.5:
                    agent.vector.scale(1.5)
                else:
                    agent.vector.scale(1/1.5)
            if random.random() >= 0.5:
                agent.vector.rotate(0.1)
            else:
                agent.vector.rotate(-0.1)
            is_hit = agent.move()
            agent.


class test(Game):

    def __init__(self,
                 title: str = 'PyGameDemo',
                 width: int = WIDTH,
                 height: int = HEIGHT,
                 fps: int = 60,
                 render: bool = True) -> None:
        super().__init__(title, width, height, fps, render)
        self.env = environment()

    def USR_loop_start(self):
        self.env.step()

    def USR_eventHandler(self):
        ...

    def USR_render(self):
        for agent in self.env.agents:
            pg.draw.rect(self.game_window, GREEN, agent.get_rect(), 2)
            pg.draw.circle(self.game_window, BLACK, agent.plane.center, 60, 1)
            pg.draw.line(self.game_window, RED,
                         agent.plane.center, agent.vector.XY, 2)


t = test()
t.mainloop()
