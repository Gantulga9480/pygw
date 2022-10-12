import pygame as pg


class Game:

    def __init__(self) -> None:
        pg.init()
        self.name: str = 'Pygame'
        self.size: tuple = (640, 480)
        self.window_flags: int = 0
        self.fps = 60
        self.running: bool = True
        self.windows = []
        self.current_window: int = 0
        self.clock = pg.time.Clock()

    def __del__(self):
        pg.quit()

    def loop_forever(self):
        while self.running:
            self.__event_handler()
            self.__render()

    def loop_once(self) -> bool:
        self.__event_handler()
        self.__render()
        return self.running

    def __event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            self.windows[self.current_window].onEvent(event)

    def __render(self):
        self.windows[self.current_window].render()

    def switch(self, window_index: int) -> None:
        if window_index < self.windows.__len__():
            self.current_window = window_index
            self.windows[self.current_window].set()
