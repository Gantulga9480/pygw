from Game import Game, BLACK, RED, GREEN
from environment import environment
from utils import *
import pygame as pg


class test(Game):

    def __init__(self,
                 title: str = 'PyGameDemo',
                 width: int = WIDTH,
                 height: int = HEIGHT,
                 fps: int = FPS,
                 render: bool = True) -> None:
        super().__init__(title, width, height, fps, render)
        self.env = environment()

    def USR_eventHandler(self):
        # print(self.env.agents[0].head.length)
        for event in self.events:
            if event.type == pg.KEYUP:
                if event.key == pg.K_w:
                    self.env.agents[0].head += 1
                elif event.key == pg.K_s:
                    self.env.agents[0].head -= 1
        if self.keys[pg.K_UP]:
            self.env.step()
        if self.keys[pg.K_LEFT]:
            self.env.agents[0].head.rotate(0.1)
        if self.keys[pg.K_RIGHT]:
            self.env.agents[0].head.rotate(-0.1)

    def USR_loop_start(self):
        # self.env.step()
        ...

    def USR_render(self):
        self.env.draw(self.window)


t = test()
t.mainloop()
