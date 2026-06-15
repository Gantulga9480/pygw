from __future__ import annotations

import pygame as pg
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .scene import Scene


class Scene:

    def __init__(self,
                 parent: 'Scene | None',
                 size: tuple[int, int],
                 position: tuple[int, int]) -> None:
        if parent is not None:
            assert isinstance(parent, Scene), \
                f"param 'parent' expected Scene, got {type(parent).__name__}"
        assert isinstance(size, (tuple, list)), \
            f"param 'size' expected tuple or list, got {type(size).__name__}"
        assert isinstance(position, (tuple, list)), \
            f"param 'position' expected tuple or list, got {type(position).__name__}"

        self.parent: 'Scene | None' = parent
        self.size: list[int] = list(size)
        self.position: list[int] = list(position)

        self.surface: pg.Surface = pg.Surface(self.size)

        self.child_scenes: list[Scene] = []
        self.visible = False
        self.draw_bb = False

    def onUpdate(self):
        pass

    def onRender(self) -> None:
        ...

    def child(self, child_index: int) -> Scene:
        return self.child_scenes[child_index]

    def add_child(self, scene: Scene) -> None:
        self.child_scenes.append(scene)

    def pop_child(self, child_index: int) -> None:
        try:
            self.child_scenes.pop(child_index)
        except IndexError:
            print("[error] - Can't remove child scene, index out of range!")

    def update(self) -> None:
        self.onUpdate()
        for child in self.child_scenes:
            if child.visible:
                child.update()

    def render(self, draw_bb: bool = False) -> None:
        self.onRender()
        if draw_bb:
            self._draw_bounding_box()
        for child in self.child_scenes:
            if child.visible:
                child.render(draw_bb)
                self.surface.blit(child.surface, child.position)

    def _draw_bounding_box(self) -> None:
        pg.draw.lines(self.surface, (255, 0, 0), True,
                      [(0, 0),
                       (0, self.size[1] - 1),
                       (self.size[0] - 1, self.size[1] - 1),
                       (self.size[0] - 1, 0)])
