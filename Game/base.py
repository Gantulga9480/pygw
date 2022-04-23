import pygame as pg    # noqa
from .color import *   # noqa
from .utils import *   # noqa


class Game:

    def __init__(self,
                 title: str = 'PyGameDemo',
                 width: int = 640,
                 height: int = 480,
                 fps: int = 60,
                 render: bool = True) -> None:
        pg.init()

        # Main window
        self.width: int = width
        self.height: int = height
        self.fps: int = fps
        self.title: str = title
        self.backgroundColor: pg.Color = WHITE
        self.running: bool = True
        self.rendering: bool = render
        self.clock = pg.time.Clock()

        # Event
        self.mouse_x = 0
        self.mouse_y = 0
        self.events = []
        self.keys = []

        # Render
        self.sprites: list[pg.Rect] = []

        # Class method implementation flags
        self.__is_setup = True
        self.__is_eventHandler = True
        self.__is_render = True

        # Utils
        self.log = True

    def __del__(self):
        pg.quit()

    def mainloop(self):
        self.__highLevelSetup()
        while self.running:
            self.USR_loop_start()
            self.__highLevelEventHandler()
            self.__highLevelRender()
            self.USR_loop_end()

    def USR_loop_start(self):
        """ User should override this method """
        ...

    def USR_loop_end(self):
        """ User should override this method """
        ...

    def __highLevelSetup(self):
        if self.__is_setup:
            try:
                self.USR_setup()
            except NotImplementedError:
                self.__is_setup = False
                LOG(level=WARNING, msg='Game setup not implemented!',
                    log=self.log)
        self.__lowLevelSetup()

    def USR_setup(self):
        """ User should override this method """
        raise NotImplementedError

    def __lowLevelSetup(self):
        self.window = self.get_window(self.width,
                                      self.height)
        self.set_title(self.title)

    def __highLevelEventHandler(self):
        if self.__lowLevelEventHandler() and self.__is_eventHandler:
            try:
                self.USR_eventHandler()
            except NotImplementedError:
                self.__is_eventHandler = False
                LOG(level=WARNING, msg='Game event handler not implemented!',
                    log=self.log)

    def USR_eventHandler(self):
        """ User should override this method """
        raise NotImplementedError

    def __lowLevelEventHandler(self):
        self.events = []
        self.mouse_x, self.mouse_y = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                break
            else:
                self.events.append(event)
        self.keys = pg.key.get_pressed()
        return self.running

    def __highLevelRender(self):
        if self.rendering and self.running:
            self.renderBackground()
            if self.__is_render:
                try:
                    self.USR_render()
                except NotImplementedError:
                    self.__is_render = False
                    LOG(level=WARNING, msg='Game rendering nothing!',
                        log=self.log)
            self.__lowLevelRender()

    def USR_render(self):
        """ User should override this method """
        raise NotImplementedError

    def renderBackground(self):
        self.window.fill(self.backgroundColor)

    def __lowLevelRender(self):
        """ TODO flip() or update() """
        if self.sprites.__len__() > 0:
            pg.display.update(self.sprites)
        else:
            pg.display.update()
        self.clock.tick(self.fps)

    @staticmethod
    def set_title(title: str):
        pg.display.set_caption(title)

    @staticmethod
    def get_window(width: int, height: int):
        """ Avoid calling outside of PyGameBase instance """
        return pg.display.set_mode((width, height))
