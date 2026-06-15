from __future__ import annotations

import os
import platform
from typing import TYPE_CHECKING

import pygame as pg

from .input_manager import InputManager
from .scene_manager import SceneManager
from .window import Window

if TYPE_CHECKING:
    from .scene import Scene


class Game:

    def __init__(self) -> None:
        if not pg.get_init():
            plat = platform.system()
            if plat == "Linux":
                pg.display.init()
                pg.font.init()
            elif plat == "Windows":
                pg.init()

        self.title: str = 'PyGameWindow'
        self.size: tuple[int, int] = (640, 480)
        self.window_flags: int = 0
        self.fps: int = 60
        self.running: bool = True
        self.rendering: bool = True
        self.clock: pg.time.Clock = pg.time.Clock()

        self.input: InputManager = InputManager()
        self.scene_manager: SceneManager = SceneManager()
        self._display_surface: pg.Surface = None

    @property
    def display_surface(self) -> pg.Surface:
        if self._display_surface is None:
            self._display_surface = pg.display.set_mode(self.size, self.window_flags)
            pg.display.set_caption(self.title)
        return self._display_surface

    @property
    def mouse_x(self) -> int:
        return self.input.mouse_x

    @property
    def mouse_y(self) -> int:
        return self.input.mouse_y

    @property
    def mouse_pos(self) -> tuple[int, int]:
        return self.input.mouse_pos

    @property
    def mouse_delta(self) -> tuple[int, int]:
        return self.input.mouse_delta

    def setup(self) -> None:
        ...

    def loop(self) -> None:
        ...

    def on_event(self, event: pg.event.Event) -> None:
        ...

    def on_render(self) -> None:
        ...

    def loop_forever(self) -> None:
        try:
            self._setup()
            while self.running:
                self._tick()
        finally:
            pg.quit()

    def loop_once(self) -> bool:
        if not self.scene_manager.active_window:
            self._setup()
        self._tick()
        return self.running

    def _setup(self) -> None:
        self.setup()
        self._tick()

    def _tick(self) -> None:
        self.input.update()
        self._handle_events()
        self.loop()
        if self.rendering and self.running:
            self.on_render()
            win = self.scene_manager.active_window
            if win is not None:
                win.update()
                win.render()
                pg.display.flip()
                self.clock.tick(self.fps)

    def _handle_events(self) -> None:
        for event in self.input.events:
            if event.type == pg.QUIT:
                self.running = False
                return
            self.on_event(event)
            win = self.scene_manager.active_window
            if win is not None:
                win.on_event(event)

    def add_window(self, window: Window) -> None:
        self.scene_manager.add_window(window)

    def remove_window(self, index: int) -> Window | None:
        return self.scene_manager.remove_window(index)

    def switch_window(self, index: int) -> Window:
        return self.scene_manager.switch_to(index)

    def get_window(self, index: int) -> Window | None:
        return self.scene_manager.get_window(index)

    @property
    def window(self) -> Window | None:
        return self.scene_manager.active_window

    @property
    def active_window(self) -> Window | None:
        return self.scene_manager.active_window

    @property
    def window_count(self) -> int:
        return self.scene_manager.window_count
