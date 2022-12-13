import pygame as pg


class Scene:

    # TODO
    # - Transparent background support

    def __init__(self,
                 parent: 'Scene',
                 size: tuple,
                 position: tuple) -> None:
        if parent is not None:
            assert isinstance(parent, (Scene)), \
                "param 'parent' Game.Scene expected, got {t}".format(
                    t=str(type(parent)).split(' ')[1].split("'")[1]
                )
        assert isinstance(size, (tuple, list)), \
            "param 'size' tuple or list expected, got {t}".format(
                t=str(type(size)).split(' ')[1].split("'")[1]
            )
        assert isinstance(position, (tuple, list)), \
            "param 'position' tuple or list expected, got {t}".format(
                t=str(type(position)).split(' ')[1].split("'")[1]
            )

        # self.parent is None in 'Base Scene'
        self.parent: Scene = parent
        self.size: list = list(size)
        self.position: list = list(position)

        # If parent is None 'Base Scene' surface will be given by Window class
        self.window: pg.Surface = None
        if self.parent is not None:
            self.window = pg.Surface(self.size)

        self.child_scenes: list[Scene] = []
        self.state: bool = True

    def onUpdate(self) -> None:
        ...

    def child(self, child_index) -> 'Scene':
        return self.child_scenes[child_index]

    def add_child(self, scene: 'Scene') -> None:
        self.child_scenes.append(scene)

    def pop_child(self, child_index) -> None:
        try:
            self.child_scenes.pop(child_index)
        except IndexError:
            print("[error] - Can't remove child scene, index out of range!")

    def render(self, draw_bb=False) -> None:
        self.onUpdate()
        if draw_bb:
            self.__draw_bounding_box()
        for scene in self.child_scenes:
            if scene.state:
                scene.render(draw_bb)
                self.window.blit(scene.window, scene.position)

    def __draw_bounding_box(self) -> None:
        pg.draw.lines(self.window, (255, 0, 0), True,
                      [(0, 0),
                       (0, self.size[1]-1),
                       (self.size[0]-1, self.size[1]-1),
                       (self.size[0]-1, 0)])
