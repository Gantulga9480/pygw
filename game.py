import platform
import pygame as pg
from .window import Window


class Game:

    def __init__(self) -> None:
        if not pg.get_init():
            os = platform.system()
            if os == "Linux":
                # On linux pg.quit hangs. Some pygame modules don't work properly on linux
                # Since we're using only display module for this package, initializing only display will do the trick
                pg.display.init()
            elif os == "Windows":
                # Windows not affected by this issue.
                pg.display.init()
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
        self.__windows: list[Window] = []
        self.window = Window(self, 0, self.title)

    def __del__(self):
        pg.quit()

    def __setup(self):
        self.window = Window(self, 0, self.title)
        self.add_window(self.window)
        self.switch(0)
        self.setup()

    def setup(self) -> None:
        """ User should override this method """
        ...

    def loop(self):
        """ User should override this method """
        ...

    def onEvent(self, event) -> None:
        """ User should override this method """
        ...

    def onRender(self) -> None:
        """ User should override this method """
        ...

    def custom_setup(self):
        self.__setup()
 
    def loop_forever(self):
        self.__setup()
        while self.running:
            self.__event_handler()
            self.loop()
            self.__render()

    def loop_once(self) -> bool:
        self.__event_handler()
        self.loop()
        self.__render()
        return self.running

    def __event_handler(self):
        self.mouse_x, self.mouse_y = pg.mouse.get_pos()
        self.keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                break
            self.onEvent(event)
            self.window.onEvent(event)

    def __render(self):
        if self.rendering and self.running:
            self.onRender()
            self.window.render()

    def add_window(self, window: Window):
        """ size, fps and flags have to be initialized before calling this function """
        self.__windows.append(window)

    def drop_window(self, index: int):
        if index == self.window.index:
            self.switch(index - 1)
        for i, window in enumerate(self.__windows):
            if window.index == index:
                win = self.__windows.pop(i)
                return win
        return None

    def switch(self, index: int):
        if index >= 0:
            for window in self.__windows:
                if window.index == index:
                    self.window = window
                    self.window.set()
                    return True
        return False
