from __future__ import annotations

from typing import Optional

from .window import Window


class SceneManager:

    def __init__(self) -> None:
        self._windows: list[Window] = []
        self._current_window_index: int = 0
        self._active_window: Optional[Window] = None

    @property
    def window_count(self) -> int:
        return len(self._windows)

    @property
    def active_window(self) -> Optional[Window]:
        return self._active_window

    @property
    def active_window_index(self) -> int:
        return self._current_window_index

    def add_window(self, window: Window) -> None:
        window.set()
        if not self._windows:
            self._current_window_index = 0
            self._active_window = window
        self._windows.append(window)

    def remove_window(self, index: int) -> Optional[Window]:
        if index < 0 or index >= len(self._windows):
            return None

        win = self._windows.pop(index)

        if index == self._current_window_index:
            self._active_window = None
            self._current_window_index = 0

        if self._windows:
            if index < self._current_window_index:
                self._current_window_index -= 1

            self._active_window = self._windows[self._current_window_index]
            self._active_window.set()

        return win

    def switch_to(self, index: int) -> Window:
        if index < 0 or index >= len(self._windows):
            raise IndexError(f"Window index {index} out of range (0-{len(self._windows) - 1})")

        self._current_window_index = index
        self._active_window = self._windows[index]
        self._active_window.set()
        return self._active_window

    def get_window(self, index: int) -> Optional[Window]:
        if 0 <= index < len(self._windows):
            return self._windows[index]
        return None

    def clear(self) -> None:
        self._windows.clear()
        self._current_window_index = 0
        self._active_window = None
