import pygame as pg
from .scene import Scene


class Window(Scene):

    def __init__(self, game, name: str = 'Pygame') -> None:
        super().__init__(None, game.size, (0, 0))
        assert isinstance(game.size, (tuple, list)), \
            "param 'size' tuple or list expected, got {t}".format(
                t=str(type(game.size)).split(' ')[1].split("'")[1]
            )
        assert isinstance(game.window_flags, int), \
            "param 'flags' int expected, got {t}".format(
                t=str(type(game.window_flags)).split(' ')[1].split("'")[1]
            )
        assert isinstance(name, str), \
            "param 'name' str expected, got {t}".format(
                t=str(type(game.window_flags)).split(' ')[1].split("'")[1]
            )
        self.game = game
        self.fps: int = game.fps
        self.name: str = name
        self.draw_bounding_boxes: bool = False

    def set(self) -> None:
        self.surface = pg.display.get_surface()
        if self.surface is None:
            self.surface = \
                pg.display.set_mode(self.size, self.game.window_flags)
        pg.display.set_caption(self.name)

    def onEvent(self, event: pg.event.Event) -> None:
        ...

    def render(self, draw_bb=False) -> None:
        self.onUpdate()
        for scene in self.child_scenes:
            if scene.state.get():
                scene.render(self.draw_bounding_boxes)
                self.surface.blit(scene.surface, scene.position)
        pg.display.flip()
        self.game.clock.tick(self.fps)
