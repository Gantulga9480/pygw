import pygame as pg    # noqa


class Game:

    def __init__(self) -> None:
        if not pg.get_init():
            pg.init()

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
        # User sprite list - TODO
        self.sprites: list[pg.Rect] = []
        # User custom render callbacks list - TODO
        self.__render_callbacks = []
        self.window = None

        self.__highLevelSetup()

    def __del__(self):
        pg.quit()

    def loop_forever(self) -> None:
        while self.running:
            self.__highLevelEventHandler()
            self.loop()
            self.__highLevelRender()

    def loop_once(self) -> bool:
        self.__highLevelEventHandler()
        self.loop()
        self.__highLevelRender()
        return self.running

    def loop(self) -> None:
        """ User should override this method """
        ...

    def __highLevelSetup(self):
        self.set_title(self.title)
        self.set_window()
        self.setup()

    def setup(self) -> None:
        """ User should override this method """
        ...

    def __highLevelEventHandler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                break
            else:
                self.onEvent(event)
        self.mouse_x, self.mouse_y = pg.mouse.get_pos()
        self.keys = pg.key.get_pressed()

    def onEvent(self, event) -> None:
        """ User should override this method """
        ...

    def __highLevelRender(self):
        if self.rendering and self.running:
            self.window.fill(self.backgroundColor)
            self.onRender()
            # TODO
            for cb in self.__render_callbacks:
                cb()
            pg.display.flip()
            self.clock.tick(self.fps)

    def onRender(self) -> None:
        """ User should override this method """
        ...

    def set_window(self, window: pg.Surface = None) -> None:
        """ Avoid calling outside of PyGameBase instance """
        if window:
            assert isinstance(window, pg.Surface)
            self.window = window
        else:
            if not self.window:
                self.window = pg.display.get_surface()
                if self.window is None:
                    self.window = pg.display.set_mode((self.width,
                                                       self.height),
                                                      self.flags)

    def get_window(self) -> pg.Surface:
        return pg.display.get_surface()

    def register_render_callback(self, func):
        self.__render_callbacks.append(func)

    @staticmethod
    def set_title(title: str) -> None:
        pg.display.set_caption(title)
