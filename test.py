from Game import Game, BLACK, RED, GREEN
from Game import CartesianPlane, Vector2D
import pygame as pg
import random


WIDTH = 1500
HEIGHT = 900


class agent:

    def __init__(self) -> None:
        self.plane = CartesianPlane((WIDTH, HEIGHT))
        self.vector = Vector2D(1, 0, self.plane)
        self.rect = None

    def get_rect(self):
        self.rect = pg.Rect(self.plane.getX(), self.plane.getY(), 0, 0).inflate(10, 10)
        return self.rect


class test(Game):

    def __init__(self,
                 title: str = 'PyGameDemo',
                 width: int = WIDTH,
                 height: int = HEIGHT,
                 fps: int = 60,
                 render: bool = True) -> None:
        super().__init__(title, width, height, fps, render)
        self.pv: list[agent] = []
        for _ in range(100):
            self.pv.append(agent())

    def USR_loop_start(self):
        print(self.game_window.get_rect().center)
        for agent in self.pv:
            if random.random() > 0.5:
                if agent.vector.length < 10:
                    agent.vector.scale(1.12)
            else:
                agent.vector.scale(0.9)
            if random.random() > 0.5:
                agent.vector.rotate(0.1)
            else:
                agent.vector.rotate(-0.1)
            agent.plane.move_with(agent.vector)

    def USR_eventHandler(self):
        if self.keys[pg.K_UP]:
            self.v.scale(1.1)
        elif self.keys[pg.K_DOWN]:
            self.v.scale(0.9)
        elif self.keys[pg.K_LEFT]:
            self.v.rotate(0.1)
        elif self.keys[pg.K_RIGHT]:
            self.v.rotate(-0.1)

    def USR_render(self):
        for agent in self.pv:
            # pg.draw.line(self.game_window, BLACK,
            #              (agent.plane.getX(agent.plane.x_lim[0]), agent.plane.getY()),
            #              (agent.plane.getX(agent.plane.x_lim[1]), agent.plane.getY()), 1)
            # pg.draw.line(self.game_window, BLACK,
            #              (agent.plane.getX(), agent.plane.getY(agent.plane.y_lim[0])),
            #              (agent.plane.getX(), agent.plane.getY(agent.plane.y_lim[1])), 1)
            pg.draw.rect(self.game_window, GREEN, agent.get_rect())
            # pg.draw.circle(self.game_window, BLACK, agent.plane.center, 100, 1)
            pg.draw.line(self.game_window, RED,
                         agent.plane.center, agent.vector.XY, 2)


t = test()
t.mainloop()
