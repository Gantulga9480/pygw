import pygame as pg
from .window import Window
import platform


class Game:

    def __init__(self) -> None:
        if not pg.get_init():
            os = platform.system()
            if os == "Linux":
                # On linux pg.quit hangs. Some pygame modules don't work properly on linux
                # Since we're using only display module for this package, initializing only display will do the trick
                pg.display.init()
            elif os == "Windows":
                # Windows not affected by this issue. So it's good to init all modules
                pg.init()
            else:
                print("[Warning] - Unknown platform, pygame not initialized")

        # Main window
        self.title: str = 'PyGameWindow'
        self.size: tuple = (640, 480)
        self.window_flags: int = 0
        self.fps: int = 60
        self.running: bool = True
        self.rendering: bool = True
        self.clock = pg.time.Clock()

        # Event
        self.mouse_x = 0
        self.mouse_y = 0
        self.keys = []

        # Render
        self.window = None
        self.__current_window: int = 0
        self.__windows: list[Window] = []

    def __del__(self):
        pg.quit()

    def __setup(self):
        self.add_window(Window(self, self. title))
        self.switch(0)
        self.setup()

    def setup(self) -> None:
        """ User should override this method """
        ...

    def onEvent(self, event) -> None:
        ...

    def onRender(self) -> None:
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
        self.mouse_x, self.mouse_y = pg.mouse.get_pos()
        self.keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            self.onEvent(event)
            self.window.onEvent(event)

    def __render(self) -> None:
        if self.rendering and self.running:
            self.onRender()
            self.window.render()

    def add_window(self, window):
        """Before calling this function size,
           flags and fps have to be initialized"""
        self.__windows.append(window)

    def drop_window(self, index: int) -> Window:
        try:
            win = self.__windows.pop(index)
            if (index == self.__current_window):
                self.window = None
            return win
        except IndexError:
            return None

    def switch(self, window_index: int) -> None:
        if 0 <= window_index < self.__windows.__len__():
            self.__current_window = window_index
            self.__windows[self.__current_window].set()
            self.window = self.__windows[self.__current_window]
        else:
            raise IndexError()
