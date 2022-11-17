from Game import Window, Scene, Game
import pygame as pg


class Test(Game):

    def __init__(self) -> None:
        super().__init__()
        self.win = Window(self)
        self.win.set()
        self.windows.append(self.win)

        self.scene = Scene(self.win, (60, 60), (300, 300))
        self.win.add_child(self.scene)

        self.win.draw_bounding_boxes = True


Test().loop_forever()
