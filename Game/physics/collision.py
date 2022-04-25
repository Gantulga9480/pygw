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
        ver1 = body1.vertices
        ver2 = body2.vertices
        for i in range(ver1.__len__()):
            tail = ver1[i-1]
            v = vector(self.space,
                       (self.space.toX(ver1[i].X) - self.space.toX(tail.X)),
                       (self.space.toY(ver1[i].Y) - self.space.toY(tail.Y)))
            normal = v.normal().unit()
            b1_cast = []
            b2_cast = []
            for ii in range(ver1.__len__()):
                if ver1[ii] is not tail:
                    ray = vector(self.space,
                                 (self.space.toX(ver1[ii].X) -
                                  self.space.toX(tail.X)),
                                 (self.space.toY(ver1[ii].Y) -
                                  self.space.toY(tail.Y)))
                    b1_cast.append(normal.dot(ray.xy))
            for ii in range(ver2.__len__()):
                ray = vector(self.space,
                             (self.space.toX(ver2[ii].X) -
                              self.space.toX(tail.X)),
                             (self.space.toY(ver2[ii].Y) -
                              self.space.toY(tail.Y)))
                b2_cast.append(normal.dot(ray.xy))
            if not self.intersect(b1_cast, b2_cast):
                return False
        for i in range(ver2.__len__()):
            tail = ver2[i-1]
            v = vector(self.space,
                       (self.space.toX(ver2[i].X) - self.space.toX(tail.X)),
                       (self.space.toY(ver2[i].Y) - self.space.toY(tail.Y)))
            normal = v.normal().unit()
            b1_cast = []
            b2_cast = []
            for ii in range(ver1.__len__()):
                ray = vector(self.space,
                             (self.space.toX(ver1[ii].X) -
                              self.space.toX(tail.X)),
                             (self.space.toY(ver1[ii].Y) -
                              self.space.toY(tail.Y)))
                b1_cast.append(normal.dot(ray.xy))
            for ii in range(ver2.__len__()):
                if ver2[ii] is not tail:
                    ray = vector(self.space,
                                 (self.space.toX(ver2[ii].X) -
                                  self.space.toX(tail.X)),
                                 (self.space.toY(ver2[ii].Y) -
                                  self.space.toY(tail.Y)))
                    b2_cast.append(normal.dot(ray.xy))
            if not self.intersect(b1_cast, b2_cast):
                return False
        return True

    def intersect(self, set1, set2):
        min1 = min(set1)
        min2 = min(set2)
        if min1 <= min2 <= max(set1):
            return True
        if min2 <= min1 <= max(set2):
            return True
        return False


class LineIntersectCollision(collision):

    def __init__(self, space: plane, side=False) -> None:
        super().__init__(space)
        self.side = side

    def collide(self, body1: shape, body2: shape):
        if not self.side:
            return self.__diagonal_intersect(body1, body2)
        return self.__side_intersect(body1, body2)

    def __diagonal_intersect(self, body1: shape, body2: shape):
        ver1 = body1.vertices
        ver2 = body2.vertices

        points = []
        for i in range(ver1.__len__()):
            tail1 = body1.position_vec.xy
            head1 = self.space.toXY(ver1[i].XY)
            for j in range(ver2.__len__()):
                tail2 = self.space.toXY(ver2[j-1].XY)
                head2 = self.space.toXY(ver2[j].XY)
                val = self.intersect(tail1, head1, tail2, head2)
                if val:
                    points.append(val)
        if points:
            return points
        for i in range(ver2.__len__()):
            tail1 = body2.position_vec.xy
            head1 = self.space.toXY(ver2[i].XY)
            for j in range(ver1.__len__()):
                tail2 = self.space.toXY(ver1[j-1].XY)
                head2 = self.space.toXY(ver1[j].XY)
                val = self.intersect(tail1, head1, tail2, head2)
                if val:
                    points.append(val)
        if points:
            return points
        return False

    def __side_intersect(self, body1: shape, body2: shape):
        ver1 = body1.vertices
        ver2 = body2.vertices

        points = []
        for i in range(ver1.__len__()):
            tail1 = self.space.toXY(ver1[i-1].XY)
            head1 = self.space.toXY(ver1[i].XY)
            for j in range(ver2.__len__()):
                tail2 = self.space.toXY(ver2[j-1].XY)
                head2 = self.space.toXY(ver2[j].XY)
                val = self.intersect(tail1, head1, tail2, head2)
                if val:
                    points.append(val)
        if points:
            return points
        for i in range(ver2.__len__()):
            tail1 = self.space.toXY(ver2[i-1].XY)
            head1 = self.space.toXY(ver2[i].XY)
            for j in range(ver1.__len__()):
                tail2 = self.space.toXY(ver1[j-1].XY)
                head2 = self.space.toXY(ver1[j].XY)
                val = self.intersect(tail1, head1, tail2, head2)
                if val:
                    points.append(val)
        if points:
            return points
        return False

    def intersect(self, p0, p1, p2, p3):
        s10_x = p1[0] - p0[0]
        s10_y = p1[1] - p0[1]
        s32_x = p3[0] - p2[0]
        s32_y = p3[1] - p2[1]
        denom = s10_x * s32_y - s32_x * s10_y
        if denom == 0.0:
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
        return intersection_point
