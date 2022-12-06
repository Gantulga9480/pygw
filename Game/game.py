import pygame as pg
from .window import Window


class Game:

    def __init__(self) -> None:
        if not pg.get_init():
            pg.init()
        self.size: tuple = (640, 480)
        self.window_flags: int = 0
        self.fps = 60
        self.running: bool = True
        self.__current_window: int = 0
        self.clock = pg.time.Clock()
        self.window: Window = None
        self.__windows: list[Window] = []

    def __del__(self):
        pg.quit()

    def __setup(self):
        self.add_window()
        if self.switch(0):
            self.setup()

    def setup(self) -> None:
        """ User should override this method """
        ...

    def loop_forever(self):
        self.__setup()
        while self.running:
            self.__event_handler()
            self.__render()

    def loop_once(self) -> bool:
        self.__event_handler()
        self.__render()
        return self.running

    def __event_handler(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            self.window.onEvent(event)

    def __render(self) -> None:
        self.window.render()

    def add_window(self, title: str = 'Pygame'):
        """Before calling this function, window size,
           flags and fps have to be initialized"""
        self.__windows.append(Window(self, title))

    def switch(self, window_index: int) -> bool:
        if window_index < self.__windows.__len__():
            self.__current_window = window_index
            self.__windows[self.__current_window].set()
            self.window = self.__windows[self.__current_window]
            return True
        return False
