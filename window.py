import pygame as pg
from .scene import Scene
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game import Game


class Window(Scene):

    def __init__(self,
                 game: 'Game',
                 index: int = 0,
                 title: str = 'Pygame'):
        super().__init__(None, game.size, (0, 0))
        self.index = index
        self.game = game
        self.title = title

    def set(self):
        self.surface = pg.display.set_mode(self.size, self.game.window_flags)
        pg.display.set_caption(self.title)

    def onEvent(self, event: pg.event.Event):
        pass

    def render(self, draw_bb=False):
        self.onUpdate()
        for scene in self.child_scenes:
            if scene.visible:
                scene.render(draw_bb or self.draw_bb)
                self.surface.blit(scene.surface, scene.position)
        pg.display.flip()
        self.game.clock.tick(self.game.fps)

    @staticmethod
    def get_surface():
        return pg.display.get_surface()

    @staticmethod
    def set_title(title: str):
        pg.display.set_caption(title)