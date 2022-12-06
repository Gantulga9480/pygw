from Game import Game, Scene


class Test(Game):

    def __init__(self) -> None:
        super().__init__()
        self.size = (1024, 720)

    def setup(self) -> None:
        self.scene = Scene(self.window, self.size, (0, 0))
        self.window.add_child(self.scene)

        self.window.draw_bounding_boxes = True
        ...


Test().loop_forever()
