import pygame as pg


class State:

    def __init__(self, state: bool = False) -> None:
        self.__var = state

    def get(self) -> bool:
        return self.__var

    def set(self, state: bool) -> None:
        self.__var = state

    def toggle(self) -> None:
        self.__var = not self.__var


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
        self.surface: pg.Surface = None
        if self.parent is not None:
            self.surface = pg.Surface(self.size)

        self.child_scenes: list[Scene] = []
        self.state: State = None

    def onUpdate(self) -> None:
        ...

    def child(self, child_index) -> 'Scene':
        return self.child_scenes[child_index]

    def add_child(self,
                  scene: 'Scene',
                  size: tuple,
                  positon: tuple,
                  state=State(True)) -> None:
        ch_scene: Scene = scene(self, size, positon)
        ch_scene.state = state
        self.child_scenes.append(ch_scene)

    def remove_child(self, child_index) -> None:
        self.child_scenes.pop(child_index)

    def render(self, draw_bb=False) -> None:
        self.onUpdate()
        if draw_bb:
            self.__draw_bounding_box()
        for scene in self.child_scenes:
            if scene.state.get():
                scene.render(draw_bb)
                self.surface.blit(scene.surface, scene.position)

    def __draw_bounding_box(self) -> None:
        pg.draw.lines(self.surface, (255, 0, 0), True,
                      [(0, 0),
                       (0, self.size[1]-1),
                       (self.size[0]-1, self.size[1]-1),
                       (self.size[0]-1, 0)])
