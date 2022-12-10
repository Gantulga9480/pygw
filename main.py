from Game import Game
from Game import core
from Game.graphic import CartesianPlane
from Game.physics import (EnginePolygon,
                          FreePolygonBody,
                          Body,
                          DynamicPolygonBody)
import numpy as np


class Test(Game):

    def __init__(self) -> None:
        super().__init__()
        self.size = (1920, 1080)
        self.window_flags = core.FULLSCREEN | core.HWSURFACE
        self.fps = 60
        self.ball_kicked = False
        self.power = 0

    def setup(self):
        self.plane = CartesianPlane(self.window, self.size, frame_rate=self.fps)
        self.p_p1 = self.plane.createPlane()
        self.p_ball = self.plane.createPlane(300, 300)
        self.p1 = DynamicPolygonBody(0, self.p_p1, (20,)*5, 11)
        self.ball = FreePolygonBody(1, self.p_ball, (5,)*10, 11, drag_coef=0.01)

        self.engine = EnginePolygon(self.plane, np.array([self.p1, self.ball], dtype=Body))

    def onEvent(self, event):
        if event.type == core.KEYUP:
            if event.key == core.K_q:
                self.running = False
            elif event.key == core.K_f:
                self.p1.detach(self.ball)
                d = self.p1.velocity.dir()
                self.ball.velocity.head = (self.power*np.cos(d), self.power*np.sin(d))
                self.ball_kicked = True
                self.power = 0
            elif event.key == core.K_g:
                self.p1.attach(self.ball, False)

    def loop(self):
        if self.keys[core.K_LEFT]:
            self.p1.rotate(5)
        if self.keys[core.K_RIGHT]:
            self.p1.rotate(-5)
        if self.keys[core.K_UP]:
            self.p1.accelerate(5)
        if self.keys[core.K_DOWN]:
            self.p1.accelerate(-5)

        if self.keys[core.K_f]:
            self.power += 0.1

        self.engine.step()

        d = self.p1.shape.plane.get_parent_vector().distance_to(self.ball.shape.plane.get_parent_vector())
        if (d <= (self.p1.radius + self.ball.radius)):
            if self.ball_kicked:
                pass
            else:
                if not self.ball.is_attached:
                    self.p1.attach(self.ball, False)
        else:
            self.ball_kicked = False

    def onRender(self):
        self.window.fill((255, 255, 255))
        self.p1.show(velocity=True)
        self.ball.show()


Test().loop_forever()
