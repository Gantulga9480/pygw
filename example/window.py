import random
from pygw import Game, Scene, Window, core


class SC(Scene):

    def __init__(self, parent: 'Scene', size: tuple, position: tuple) -> None:
        super().__init__(parent, size, position)

    def onUpdate(self) -> None:
        b = random.randint(0, 100)
        self.window.fill((255, 255, b))


class SC1(Scene):

    def __init__(self, parent: 'Scene', size: tuple, position: tuple) -> None:
        super().__init__(parent, size, position)

    def onUpdate(self) -> None:
        b = random.randint(0, 100)
        self.window.fill((255, 0, b))


class Win(Window):

    def __init__(self, game, title: str = 'Pygame') -> None:
        super().__init__(game, title)
        self.set()
        self.add_child(SC(self, (300, 300), (100, 100)))

    def onUpdate(self) -> None:
        g = random.randint(0, 100)
        self.window.fill((0, g, 0))


class Win1(Window):

    def __init__(self, game, title: str = 'Pygame') -> None:
        super().__init__(game, title)
        self.add_child(SC1(self, (300, 300), (500, 100)))

    def onUpdate(self) -> None:
        r = random.randint(0, 100)
        self.window.fill((r, 0, 0))


class Test(Game):

    def __init__(self) -> None:
        super().__init__()
        self.size = (1024, 720)

    def setup(self) -> None:
        custom_main = Win(self, 'test-main')
        self.drop_window(0)  # drop default window
        self.add_window(custom_main)  # create custom main window
        self.switch(0)  # set main window, window at position 0 will always be main window

        custom_window = Win1(self, 'test-second')
        self.add_window(custom_window)

        custom_main.enableBB()
        custom_window.enableBB()

    def onEvent(self, event) -> None:
        if event.type == core.KEYUP:
            if event.key == core.K_1:
                self.switch(0)
            elif event.key == core.K_2:
                self.switch(1)


Test().loop_forever()
