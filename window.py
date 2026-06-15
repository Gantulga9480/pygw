from __future__ import annotations

import pygame as pg
from .scene import Scene
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game import Game


class Window(Scene):

    def __init__(self, game: 'Game', title: str = 'Pygame') -> None:
        super().__init__(None, game.size, (0, 0))
        assert isinstance(game.size, (tuple, list)), \
            f"param 'size' expected tuple or list, got {type(size).__name__}"
        assert isinstance(game.window_flags, int), \
            f"param 'flags' expected int, got {type(game.window_flags).__name__}"
        assert isinstance(title, str), \
            f"param 'title' expected str, got {type(title).__name__}"

        self.game: Game = game
        self.title: str = title
        self._draw_bounding_boxes: bool = False

    def set(self) -> None:
        self.surface = self.game.display_surface
        pg.display.set_caption(self.title)

    def on_event(self, event: pg.event.Event) -> None:
        ...

    def render(self, draw_bb: bool = False) -> None:
        super().render(draw_bb or self._draw_bounding_boxes)

    def enable_bb(self) -> None:
        self._draw_bounding_boxes = True

    def disable_bb(self) -> None:
        self._draw_bounding_boxes = False

    @staticmethod
    def get_surface() -> pg.Surface | None:
        return pg.display.get_surface()

    @staticmethod
    def set_title(title: str) -> None:
        pg.display.set_caption(title)
