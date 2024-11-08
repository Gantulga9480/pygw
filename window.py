import pygame as pg
from .scene import Scene

class Window(Scene):

    def __init__(self, game, title: str = 'Pygame') -> None:
        super().__init__(None, game.size, (0, 0))
        assert isinstance(game.size, (tuple, list)), \
            "param 'size' tuple or list expected, got {t}".format(
                t=str(type(game.size)).split(' ')[1].split("'")[1]
            )
        assert isinstance(game.window_flags, int), \
            "param 'flags' int expected, got {t}".format(
                t=str(type(game.window_flags)).split(' ')[1].split("'")[1]
            )
        assert isinstance(title, str), \
            "param 'title' str expected, got {t}".format(
                t=str(type(title)).split(' ')[1].split("'")[1]
            )

        self.game = game
        self.title: str = title
        self.__draw_bounding_boxes: bool = False

    def set(self) -> None:
        self.surface = pg.display.get_surface()
        if self.surface is None:
            self.surface = \
                pg.display.set_mode(self.size, self.game.window_flags)
        pg.display.set_caption(self.title)

    def onEvent(self, event: pg.event.Event) -> None:
        ...

    def render(self) -> None:
        self.onUpdate()
        for scene in self.child_scenes:
            if scene.visible:
                scene.render(self.__draw_bounding_boxes)
                self.surface.blit(scene.surface, scene.position)
        pg.display.flip()
        self.game.clock.tick(self.game.fps)

    def enableBB(self):
        self.__draw_bounding_boxes = True

    def disableBB(self):
        self.__draw_bounding_boxes = False

    @staticmethod
    def get_surface():
        return pg.display.get_surface()

    @staticmethod
    def set_title(title: str):
        pg.display.set_caption(title)