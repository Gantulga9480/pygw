from __future__ import annotations

import pygame as pg


class InputManager:

    def __init__(self) -> None:
        self._keys_pressed: tuple[int, ...] = ()
        self._keys_pressed_prev: tuple[int, ...] = ()

        self._mouse_x: int = 0
        self._mouse_y: int = 0
        self._mouse_x_prev: int = 0
        self._mouse_y_prev: int = 0

        self._mouse_buttons: tuple[bool, bool, bool] = (False, False, False)
        self._mouse_buttons_prev: tuple[bool, bool, bool] = (False, False, False)

        self._events: list[pg.event.Event] = []

    def update(self) -> None:
        self._keys_pressed_prev = self._keys_pressed
        self._keys_pressed = pg.key.get_pressed()

        self._mouse_x_prev = self._mouse_x
        self._mouse_y_prev = self._mouse_y
        self._mouse_x, self._mouse_y = pg.mouse.get_pos()

        self._mouse_buttons_prev = self._mouse_buttons
        self._mouse_buttons = pg.mouse.get_pressed()

        self._events = pg.event.get()

    @property
    def events(self) -> list[pg.event.Event]:
        return self._events

    @property
    def mouse_x(self) -> int:
        return self._mouse_x

    @property
    def mouse_y(self) -> int:
        return self._mouse_y

    @property
    def mouse_pos(self) -> tuple[int, int]:
        return (self._mouse_x, self._mouse_y)

    @property
    def mouse_delta(self) -> tuple[int, int]:
        return (self._mouse_x - self._mouse_x_prev,
                self._mouse_y - self._mouse_y_prev)

    def is_key_pressed(self, key: int) -> bool:
        return bool(self._keys_pressed[key])

    def was_key_pressed(self, key: int) -> bool:
        return (self._keys_pressed[key] and
                not self._keys_pressed_prev[key])

    def was_key_released(self, key: int) -> bool:
        return (not self._keys_pressed[key] and
                self._keys_pressed_prev[key])

    def is_mouse_button_pressed(self, button: int = 0) -> bool:
        return bool(self._mouse_buttons[button])

    def was_mouse_button_pressed(self, button: int = 0) -> bool:
        return (self._mouse_buttons[button] and
                not self._mouse_buttons_prev[button])

    def was_mouse_button_released(self, button: int = 0) -> bool:
        return (not self._mouse_buttons[button] and
                self._mouse_buttons_prev[button])

    def contains_event_type(self, event_type: int) -> bool:
        return any(e.type == event_type for e in self._events)

    def get_events_of_type(self, event_type: int) -> list[pg.event.Event]:
        return [e for e in self._events if e.type == event_type]
