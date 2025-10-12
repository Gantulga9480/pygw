import random
from pygw import Game, Scene, Window, core


class SC(Scene):

    def __init__(self, parent: 'Scene', size: tuple, position: tuple) -> None:
        super().__init__(parent, size, position)
        self.visible = True

    def onUpdate(self) -> None:
        self.surface.fill((255, 255, 0))


class SC1(Scene):

    def __init__(self, parent: 'Scene', size: tuple, position: tuple) -> None:
        super().__init__(parent, size, position)
        self.visible = True

    def onUpdate(self) -> None:
        self.surface.fill((255, 0, 0))


class Win(Window):

    def __init__(self, game, index: int = 0, title: str = 'Pygame') -> None:
        super().__init__(game, index, title)
        self.add_child(SC(self, (300, 300), (100, 100)))
        self.draw_bb = True

    def onUpdate(self) -> None:
        self.surface.fill((0, 100, 0))


class Win1(Window):

    def __init__(self, game, index: int = 0, title: str = 'Pygame') -> None:
        super().__init__(game, index, title)
        self.add_child(SC1(self, (300, 300), (500, 100)))
        self.draw_bb = True

    def onUpdate(self) -> None:
        self.surface.fill((100, 0, 0))


class Test(Game):

    WINDOW1_ID=0
    WINDOW2_ID=1

    def __init__(self) -> None:
        super().__init__()
        self.size = (1024, 768)

    def setup(self) -> None:
        custom_main = Win(self, self.WINDOW1_ID, 'test-main')
        self.drop_window(0)  # drop default window
        self.add_window(custom_main)  # create custom main window
        self.switch(self.WINDOW1_ID)  # set main window, window with id 0 will always be the main window

        custom_window = Win1(self, self.WINDOW2_ID, 'test-second')
        self.add_window(custom_window)

    def onEvent(self, event) -> None:
        if event.type == core.KEYUP:
            if event.key == core.K_1:
                self.switch(self.WINDOW1_ID)
            elif event.key == core.K_2:
                self.switch(self.WINDOW2_ID)


if __name__ == "__main__":
    Test().loop_forever()
