from Game.graphic.cartesian import CartesianPlane, Vector2d
from Game.physics.body import DYNAMIC, STATIC
from Game.graphic.shapes import shape


class collision:

    def __init__(self,
                 space: CartesianPlane,
                 resolver=None) -> None:
        self.space = space
        self.__resolve = resolver

    def static_collision(self, body1: shape, body2: shape):
        raise NotImplementedError

    def dynamic_collision(self, body1: shape, body2: shape):
        raise NotImplementedError

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

    def static_collision(self, body1: shape, body2: shape):
        self.__resolve = self.static_resolver  # TODO
        if not self.side:
            # check collision using vertex diagonals, resolve collision
            self.__resolve(*self.__diagonal_intersect(body1, body2))
        else:
            # check collision using side edges, resolve collision
            self.__resolve(*self.__side_intersect(body1, body2))

    def dynamic_collision(self, body1: shape, body2: shape):
        if not self.side:
            # check collision using vertex diagonals, resolve collision
            self.__resolve(self.__diagonal_intersect(body1, body2))
            return
        # check collision using side edges resolve collision
        self.__resolve(self.__side_intersect(body1, body2))
        return

    def static_resolver(self, body: shape, displacement):
        body.vec.x -= displacement[0]
        body.vec.y -= displacement[1]

    def __diagonal_intersect(self, body1: shape, body2: shape):
        b1 = body1
        b2 = body2
        db = [0, 0]
        for i in range(b1.vertices.__len__()):
            # check for every vertex of first shape against ...
            l1s = self.space.toXY(b1.plane.CENTER)
            l1e = self.space.toXY(b1.vertices[i].HEAD)
            for j in range(b2.vertices.__len__()):
                # ... every edge of second shape
                l2s = self.space.toXY(b2.vertices[j-1].HEAD)
                l2e = self.space.toXY(b2.vertices[j].HEAD)
                # check these two line segments are intersecting or not
                val = self.line_segment_intersect(l1s, l1e, l2s, l2e)
                if val:
                    db[0] += b1.vertices[i].x * val[1]
                    db[1] += b1.vertices[i].y * val[1]
        return b1, db

    def __side_intersect(self, body1: shape, body2: shape):
        points = []
        for i in range(body1.vertices.__len__()):
            l1s = self.space.toXY(body1.vertices[i-1].HEAD)
            l1e = self.space.toXY(body1.vertices[i].HEAD)
            for j in range(body2.vertices.__len__()):
                l2s = self.space.toXY(body2.vertices[j-1].HEAD)
                l2e = self.space.toXY(body2.vertices[j].HEAD)
                val = self.line_segment_intersect(l1s, l1e, l2s, l2e)
                if val:
                    points.append(val)
        return points


class SeparatingAxisTheorem(collision):

    def __init__(self, space: CartesianPlane) -> None:
        super().__init__(space)

    def collide(self, body1: shape, body2: shape):
        # TODO
        ...
