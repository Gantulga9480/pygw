from Game.graphic.cartesian import vector, plane
from Game.graphic.shapes import shape


class collision:

    def __init__(self, space: plane) -> None:
        self.space = space

    def collide(self, body1: shape, body2: shape):
        raise NotImplementedError


class SeparatingAxisTheorem(collision):

    def __init__(self, space: plane) -> None:
        super().__init__(space)

    def collide(self, body1: shape, body2: shape):
        for i, vertex in enumerate(body1.vertices):
            tail = body1.vertices[i-1]
            v = vector(self.space,
                       (self.space.toX(vertex.X) - self.space.toX(tail.X)),
                       (self.space.toY(vertex.Y) - self.space.toY(tail.Y)))
            normal = v.normal().unit()
            b1_cast = []
            b2_cast = []
            for ver in body1.vertices:
                if ver is not tail:
                    ray = vector(self.space,
                                 (self.space.toX(ver.X) -
                                  self.space.toX(tail.X)),
                                 (self.space.toY(ver.Y) -
                                  self.space.toY(tail.Y)))
                    b1_cast.append(normal.dot(ray))
            for ver in body2.vertices:
                ray = vector(self.space,
                             (self.space.toX(ver.X) -
                              self.space.toX(tail.X)),
                             (self.space.toY(ver.Y) -
                              self.space.toY(tail.Y)))
                b2_cast.append(normal.dot(ray))
            if not self.intersect(b1_cast, b2_cast):
                return False
        for i, vertex in enumerate(body2.vertices):
            tail = body2.vertices[i-1]
            v = vector(self.space,
                       (self.space.toX(vertex.X) - self.space.toX(tail.X)),
                       (self.space.toY(vertex.Y) - self.space.toY(tail.Y)))
            normal = v.normal().unit()
            b1_cast = []
            b2_cast = []
            for ver in body1.vertices:
                ray = vector(self.space,
                             (self.space.toX(ver.X) -
                              self.space.toX(tail.X)),
                             (self.space.toY(ver.Y) -
                              self.space.toY(tail.Y)))
                b1_cast.append(normal.dot(ray))
            for ver in body2.vertices:
                if ver is not tail:
                    ray = vector(self.space,
                                 (self.space.toX(ver.X) -
                                  self.space.toX(tail.X)),
                                 (self.space.toY(ver.Y) -
                                  self.space.toY(tail.Y)))
                    b2_cast.append(normal.dot(ray))
            if not self.intersect(b1_cast, b2_cast):
                return False
        return True

    def intersect(self, set1, set2):
        min1 = min(set1)
        max1 = max(set1)
        min2 = min(set2)
        max2 = max(set2)
        if min1 <= min2 <= max1:
            return True
        if min2 <= min1 <= max2:
            return True
        return False
