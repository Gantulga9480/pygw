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


class Test(Game):

    def __init__(self) -> None:
        super().__init__()
        self.size = (1024, 720)

    def setup(self) -> None:
        self.scene = SC(self.window, (300, 300), (100, 100))
        self.scene1 = SC1(self.window, (300, 300), (500, 100))
        self.window.add_child(self.scene)
        self.window.add_child(self.scene1)

        self.window1 = Window(self, 'test')
        self.add_window(self.window1)
        self.window1.add_child(SC(self.window, (200, 200), (100, 100)))
        self.window1.add_child(SC1(self.window, (200, 200), (500, 100)))

        self.window.draw_bounding_boxes = True
        self.window1.draw_bounding_boxes = True

    def onEvent(self, event) -> None:
        if event.type == core.KEYUP:
            if event.key == core.K_1:
                self.switch(0)
            elif event.key == core.K_2:
                self.switch(1)


Test().loop_forever()
