from Game import Game, Scene, Window, core


class SC(Scene):

    def __init__(self, parent: 'Scene', size: tuple, position: tuple) -> None:
        super().__init__(parent, size, position)

    def onUpdate(self) -> None:
        self.window.fill((255, 255, 255))


class SC1(Scene):

    def __init__(self, parent: 'Scene', size: tuple, position: tuple) -> None:
        super().__init__(parent, size, position)

    def onUpdate(self) -> None:
        self.window.fill((255, 0, 255))


class Win(Window):

    def __init__(self, game, title: str = 'Pygame') -> None:
        super().__init__(game, title)
        self.add_child(SC(self.window, (300, 300), (100, 100)))

    def onUpdate(self) -> None:
        self.window.fill((0, 0, 0))


class Test(Game):

    def __init__(self) -> None:
        super().__init__()
        self.size = (1024, 720)

    def setup(self) -> None:
        self.drop_window(0)  # drop default window
        self.add_window(Win(self, 'test-main'))  # create custom window
        self.switch(0)  # set main window, window at position 0 will always be main window

        self.window1 = Win(self, 'test-second')
        self.add_window(self.window1)
        self.window.draw_bounding_boxes = True
        self.window1.draw_bounding_boxes = True

    def onEvent(self, event) -> None:
        if event.type == core.KEYUP:
            if event.key == core.K_1:
                self.switch(0)
            elif event.key == core.K_2:
                self.switch(1)


Test().loop_forever()
