from Game import Game
from Game import core
from Game.graphic import CartesianPlane
from Game.physics import (EnginePolygon,
                          FreePolygonBody,
                          object_body,
                          DynamicPolygonBody)
import numpy as np


class Test(Game):

    def __init__(self) -> None:
        super().__init__()
        self.size = (1920, 1080)
        self.window_flags = core.FULLSCREEN | core.HWSURFACE
        self.fps = 60

    def setup(self):
        self.plane = CartesianPlane(self.window, self.size, frame_rate=self.fps)
        self.p_p1 = self.plane.createPlane()
        self.p_ball = self.plane.createPlane(300, 300)
        self.p1 = DynamicPolygonBody(0, self.p_p1, (10,)*10, 11)
        self.ball = FreePolygonBody(1, self.p_ball, (3,)*10, 11, drag_coef=0.01)

        self.p1.attach(self.ball, False)
        self.engine = EnginePolygon(self.plane, np.array([self.p1, self.ball], dtype=object_body))

    def onEvent(self, event):
        if event.type == core.KEYUP:
            if event.key == core.K_q:
                self.running = False

    def loop(self):
        if self.keys[core.K_f]:
            self.p1.detach(self.ball)
        if self.keys[core.K_g]:
            self.p1.attach(self.ball, False)

        if self.keys[core.K_LEFT]:
            self.p1.rotate(10)
        if self.keys[core.K_RIGHT]:
            self.p1.rotate(-10)
        if self.keys[core.K_UP]:
            self.p1.accelerate(5)
        if self.keys[core.K_DOWN]:
            self.p1.accelerate(-5)

        if self.keys[core.K_a]:
            self.ball.rotate(1)
        if self.keys[core.K_d]:
            self.ball.rotate(-1)
        if self.keys[core.K_w]:
            self.ball.accelerate(10)
        if self.keys[core.K_s]:
            self.ball.accelerate(-10)

        self.engine.step()

    def onRender(self):
        self.window.fill((255, 255, 255))
        self.plane.show()
        self.p1.show(velocity=True)
        self.ball.show()


Test().loop_forever()
