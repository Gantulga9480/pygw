from Game.graphic.cartesian import CartesianPlane
from Game.physics.body import DYNAMIC, STATIC, base_body


class collision:

    def __init__(self,
                 space: CartesianPlane,
                 resolver=None) -> None:
        self.space = space
        self._resolve = self.static_resolve
        self._dynamic_resolver = resolver

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

    def line_segment_intersect(self, p0, p1, p2, p3):
        s10_x = p1[0] - p0[0]
        s10_y = p1[1] - p0[1]
        s32_x = p3[0] - p2[0]
        s32_y = p3[1] - p2[1]
        denom = s10_x * s32_y - s32_x * s10_y
        if denom == 0:
            return None  # collinear
        denom_is_positive = denom > 0
        s02_x = p0[0] - p2[0]
        s02_y = p0[1] - p2[1]
        s_numer = s10_x * s02_y - s10_y * s02_x
        if (s_numer < 0) == denom_is_positive:
            return None  # no collision
        t_numer = s32_x * s02_y - s32_y * s02_x
        if (t_numer < 0) == denom_is_positive:
            return None  # no collision
        if (s_numer > denom) == denom_is_positive or \
                (t_numer > denom) == denom_is_positive:
            return None  # no collision
        # collision detected
        t = t_numer / denom
        intersection_point = [p0[0] + (t * s10_x), p0[1] + (t * s10_y)]
        return intersection_point, 1-t

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
        self._resolve = self.static_resolve
        # check collision using vertex diagonals, resolve collision
        return self.__diagonal_intersect(body1, body2)

    def dynamic_collision(self, body1: base_body, body2: base_body):
        self._resolve = self._dynamic_resolver
        # check collision using vertex diagonals, resolve collision
        return self.__diagonal_intersect(body1, body2)

    def __diagonal_intersect(self, body1: base_body, body2: base_body):
        b1 = body1
        b2 = body2
        points = []
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
                        points.append(self.space.getXY(val[0]))
                        d[0] += (l1e[0] - l1s[0]) * val[1]
                        d[1] += (l1e[1] - l1s[1]) * val[1]
                if d[0] != 0 or d[1] != 0:
                    self._resolve(b1, b2, d)
        return points


class SeparatingAxisTheorem(collision):

    def __init__(self, space: CartesianPlane) -> None:
        super().__init__(space)

    def collide(self, body1: base_body, body2: base_body):
        # TODO
        ...
