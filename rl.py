from Game.graphic.cartesian import scalar, plane, vector
from Game import BLACK, RED, BLUE
from utils import *
import pygame as pg
import random
import math


class MainPlane(plane):

    def __init__(self, size, unit_length=1) -> None:
        super().__init__(size, unit_length)


class ObjectPlane(plane):

    def __init__(self, size, unit_length=1) -> None:
        super().__init__(size, unit_length)


class AgentPlane(plane):

    def __init__(self,
                 size: tuple,
                 unit_length=1) -> None:
        super().__init__(size, unit_length)

    def move(self, vec: vector):
        d = vec.length / FPS * self.unit_length
        vx = math.cos(vec.direction) * d
        vy = math.sin(vec.direction) * d
        self.X += vx
        self.Y -= vy
        if self.X == 0 or self.X == self._size[0] or \
                self.Y == 0 or self.Y == self._size[1]:
            return True
        return False


class agent:

    def __init__(self, x, y) -> None:
        self.plane = AgentPlane((WIDTH, HEIGHT))
        self.vector = self.plane.vector(x, y)

    def move(self):
        return self.plane.move(self.vector)

    @property
    def rect(self):
        return pg.Rect(self.plane.getX(),
                       self.plane.getY(), 0, 0).inflate(30, 30)

    @property
    def position(self):
        return self.plane.center


class environment:

    def __init__(self, num_agents=1) -> None:
        self.plane = MainPlane((WIDTH, HEIGHT))
        self.agents: list[agent] = []
        self.speeds = [1/1.3, 1/1.25, 1/1.2, 1/1.15, 1/1.1, 1,
                       1.1, 1.15, 1.2, 1.25, 1.3]
        self.ro_speeds = [-math.pi/8, -math.pi/16, -math.pi/32, -math.pi/64, 0,
                          math.pi/64, math.pi/32, math.pi/16, math.pi/8]
        for _ in range(num_agents):
            self.agents.append(agent(FPS, 0))

    def step(self):
        ...

    def step(self):
        for agent in self.agents:
            if FPS//4 <= agent.vector.length <= FPS*4:
                agent.vector *= random.choice(self.speeds)
            agent.vector.rotate(random.choice(self.ro_speeds))
            is_hit = agent.move()
            if is_hit:
                agent.vector.rotate(math.pi)

    def draw(self, parent):
        for agent in self.agents:
            # pg.draw.line(self.window, BLACK, self.env.plane.center,
            #              agent.get_rect().center)
            pg.draw.circle(parent, BLUE, agent.rect.center, 10)
            pg.draw.circle(parent, BLACK, agent.rect.center, FPS, 1)
            pg.draw.line(parent, RED, agent.rect.center,
                         agent.vector.XY, 2)

    def __get_agents_pos(self):
        pos = []
        for agent in self.agents:
            pos.append(self.plane.toCenter(agent.position))
