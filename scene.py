import pygame as pg


class Scene:

    # TODO
    # - Transparent background support

    def __init__(self,
                 parent: 'Scene | None',
                 size: tuple[int, int],
                 position: tuple[int, int]):
        self.parent = parent
        self.size = list(size)
        self.position = list(position)

        self.surface: pg.Surface = pg.Surface(self.size)

        self.child_scenes: list[Scene] = []
        self.visible = False
        self.draw_bb = False

    def onUpdate(self):
        pass

    def child(self, child_index: int):
        return self.child_scenes[child_index]

    def add_child(self, scene: 'Scene'):
        self.child_scenes.append(scene)

    def pop_child(self, child_index: int):
        return self.child_scenes.pop(child_index)

    def render(self, draw_bb=False):
        self.onUpdate()
        if draw_bb or self.draw_bb:
            self.__draw_bounding_box()
        for scene in self.child_scenes:
            if scene.visible:
                scene.render(draw_bb)
                self.surface.blit(scene.surface, scene.position)

    def __draw_bounding_box(self):
        pg.draw.lines(self.surface, (255, 0, 0), True,
                      [(0, 0),
                       (0, self.size[1]-1),
                       (self.size[0]-1, self.size[1]-1),
                       (self.size[0]-1, 0)])
