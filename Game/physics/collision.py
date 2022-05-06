from Game.graphic.cartesian import CartesianPlane
from Game.physics.body import DYNAMIC, STATIC, base_body


class collision:

    def __init__(self,
                 space: CartesianPlane,
                 resolver=None) -> None:
        self.space = space
        self.__resolve = resolver

    def static_collision(self, body1: base_body, body2: base_body):
        raise NotImplementedError

    def dynamic_collision(self, body1: base_body, body2: base_body):
        raise NotImplementedError

    def static_resolve(self, b1: base_body, b2: base_body, d: tuple):
        if b1.body.state == DYNAMIC and b2.body.state == STATIC:
            b1.vec.x -= d[0]
            b1.vec.y -= d[1]
        elif b1.body.state == STATIC and b2.body.state == DYNAMIC:
            b2.vec.x += d[0]
            b2.vec.y += d[1]
        elif b1.body.state == DYNAMIC and b2.body.state == DYNAMIC:
            b1.vec.x -= d[0]/2
            b1.vec.y -= d[1]/2
            b2.vec.x += d[0]/2
            b2.vec.y += d[1]/2

    def line_segment_intersect(self, l1s, l1e, l2s, l2e):
        l1_x = l2e[0] - l2s[0]
        l1_y = (l1s[1] - l1e[1])
        h = l1_x * l1_y - (l1s[0] - l1e[0]) * (l2e[1] - l2s[1])
        if h == 0.0:
            return False
        t1 = ((l2s[1] - l2e[1]) * (l1s[0] - l2s[0]) +
              (l1_x) * (l1s[1] - l2s[1])) / h
        t2 = (l1_y * (l1s[0] - l2s[0]) +
              (l1e[0] - l1s[0]) * (l1s[1] - l2s[1])) / h

        if t1 >= 0.0 and t1 < 1.0 and t2 >= 0.0 and t2 < 1.0:
            # TODO FIX intersection point
            return ([l1s[0] + (t1 * l1_x), l1s[1] + (t1 * (l1e[1] - l1s[1]))],
                    (1 - t1))
        return False

    def point_set_intersect(self, set1, set2):
        min1 = min(set1)
        min2 = min(set2)
        if min1 <= min2 <= max(set1):
            return True
        if min2 <= min1 <= max(set2):
            return True
        return False


class LineIntersectCollision(collision):

    def __init__(self,
                 space: CartesianPlane,
                 resolver=None,
                 side=False) -> None:
        super().__init__(space, resolver)
        self.side = side

    def static_collision(self, body1: base_body, body2: base_body):
        self.__resolve = self.static_resolve
        # check collision using vertex diagonals, resolve collision
        self.__diagonal_intersect(body1, body2)

    def dynamic_collision(self, body1: base_body, body2: base_body):
        # check collision using vertex diagonals, resolve collision
        ...

    def __diagonal_intersect(self, body1: base_body, body2: base_body):
        b1 = body1
        b2 = body2
        for i in range(2):
            if i == 1:
                b1 = body2
                b2 = body1
            for i in range(b1.vertices.__len__()):
                # check for every vertex of first shape against ...
                l1s = self.space.toXY(b1.plane.CENTER)
                l1e = self.space.toXY(b1.vertices[i].HEAD)
                d = [0, 0]
                for j in range(b2.vertices.__len__()):
                    # ... every edge of second shape
                    l2s = self.space.toXY(b2.vertices[j-1].HEAD)
                    l2e = self.space.toXY(b2.vertices[j].HEAD)
                    # check these two line segments are intersecting or not
                    val = self.line_segment_intersect(l1s, l1e, l2s, l2e)
                    if val:
                        d[0] += (l1e[0] - l1s[0]) * val[1]
                        d[1] += (l1e[1] - l1s[1]) * val[1]
                self.__resolve(b1, b2, d)


class SeparatingAxisTheorem(collision):

    def __init__(self, space: CartesianPlane) -> None:
        super().__init__(space)

    def collide(self, body1: base_body, body2: base_body):
        # TODO
        ...
