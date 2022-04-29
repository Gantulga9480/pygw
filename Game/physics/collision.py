from Game.graphic.cartesian import CartesianPlane, Vector2d
from Game.physics.body import body, DYNAMIC, STATIC


class collision:

    def __init__(self, space: CartesianPlane) -> None:
        self.space = space

    def collide(self, body1: body, body2: body):
        raise NotImplementedError

    def line_segment_intersect(self, line_s, line_e, line2_s, line2_e):
        raise NotImplementedError

    def point_set_intersect(self, points1, points2):
        raise NotImplementedError


class LineIntersectCollision(collision):

    def __init__(self, space: CartesianPlane, side=False) -> None:
        super().__init__(space)
        self.side = side

    def collide(self, body1: body, body2: body):
        if not self.side:
            # check collision using vertex diagonals
            return self.__diagonal_intersect(body1, body2)
        # check collision using side edges
        return self.__side_intersect(body1, body2)

    def __diagonal_intersect(self, body1: body, body2: body):
        b1 = body1
        b2 = body2
        for k in range(2):
            if k == 1:
                b1 = body2
                b2 = body1
            for i in range(b1.vertices.__len__()):
                # check for every vertex of first shape against ...
                l1s = self.space.toXY(b1.position_vec.HEAD)
                l1e = self.space.toXY(b1.vertices[i].HEAD)
                db = [0, 0]
                for j in range(b2.vertices.__len__()):
                    # ... every edge of second shape
                    l2s = self.space.toXY(b2.vertices[j-1].HEAD)
                    l2e = self.space.toXY(b2.vertices[j].HEAD)
                    # check these two line segments are intersecting or not
                    val = self.line_segment_intersect(l1s, l1e, l2s, l2e)
                    if val:
                        db[0] += b1.vertices[i].x * val[1]
                        db[1] += b1.vertices[i].y * val[1]
                if b1.state == DYNAMIC and b2.state == STATIC:
                    b1.position_vec.x -= db[0]
                    b1.position_vec.y -= db[1]
                elif b1.state == STATIC and b2.state == DYNAMIC:
                    b2.position_vec.x += db[0]
                    b2.position_vec.y += db[1]
        return False

    def __side_intersect(self, body1: body, body2: body):
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


class SeparatingAxisTheorem(collision):

    def __init__(self, space: CartesianPlane) -> None:
        super().__init__(space)

    def collide(self, body1: body, body2: body):
        ver1 = body1.vertices
        ver2 = body2.vertices
        for i in range(ver1.__len__()):
            tail = ver1[i-1]
            v = Vector2d(self.space,
                         (self.space.toX(ver1[i].X) - self.space.toX(tail.X)),
                         (self.space.toY(ver1[i].Y) - self.space.toY(tail.Y)))
            normal = v.normal().unit()
            b1_cast = []
            b2_cast = []
            for ii in range(ver1.__len__()):
                if ver1[ii] is not tail:
                    ray = Vector2d(self.space,
                                   (self.space.toX(ver1[ii].X) -
                                    self.space.toX(tail.X)),
                                   (self.space.toY(ver1[ii].Y) -
                                    self.space.toY(tail.Y)))
                    b1_cast.append(normal.dot(ray.xy))
            for ii in range(ver2.__len__()):
                ray = Vector2d(self.space,
                               (self.space.toX(ver2[ii].X) -
                                self.space.toX(tail.X)),
                               (self.space.toY(ver2[ii].Y) -
                                self.space.toY(tail.Y)))
                b2_cast.append(normal.dot(ray.xy))
            if not self.point_intersect(b1_cast, b2_cast):
                return False
        for i in range(ver2.__len__()):
            tail = ver2[i-1]
            v = Vector2d(self.space,
                         (self.space.toX(ver2[i].X) - self.space.toX(tail.X)),
                         (self.space.toY(ver2[i].Y) - self.space.toY(tail.Y)))
            normal = v.normal().unit()
            b1_cast = []
            b2_cast = []
            for ii in range(ver1.__len__()):
                ray = Vector2d(self.space,
                               (self.space.toX(ver1[ii].X) -
                                self.space.toX(tail.X)),
                               (self.space.toY(ver1[ii].Y) -
                                self.space.toY(tail.Y)))
                b1_cast.append(normal.dot(ray.xy))
            for ii in range(ver2.__len__()):
                if ver2[ii] is not tail:
                    ray = Vector2d(self.space,
                                   (self.space.toX(ver2[ii].X) -
                                    self.space.toX(tail.X)),
                                   (self.space.toY(ver2[ii].Y) -
                                    self.space.toY(tail.Y)))
                    b2_cast.append(normal.dot(ray.xy))
            if not self.point_intersect(b1_cast, b2_cast):
                return False
        return True

    def point_set_intersect(self, set1, set2):
        min1 = min(set1)
        min2 = min(set2)
        if min1 <= min2 <= max(set1):
            return True
        if min2 <= min1 <= max(set2):
            return True
        return False
