import math


class scalar:

    def __init__(self, value=0, limits=None) -> None:
        self.limits = limits
        if value < self.limits[0]:
            self.value = self.limits[0]
        elif value > self.limits[1]:
            self.value = self.limits[1]
        else:
            self.value = value

    def __add__(self, o: object):
        if self.limits:
            if self.value + o <= self.limits[1]:
                self.value += o
            else:
                self.value = self.limits[1]
        else:
            self.value += o
        return self

    def __sub__(self, o: object):
        print(self.value, o)
        if self.limits:
            if self.value - o >= self.limits[0]:
                self.value -= o
            else:
                self.value = 0
        else:
            self.value -= o
        return self

    def __mul__(self, o: object):
        if self.limits:
            if self.value * o <= self.limits[1]:
                self.value *= o
            else:
                self.value = self.limits[1]
        else:
            self.value *= o
        return self

    def __truediv__(self, o: object):
        if self.limits:
            if self.value / o <= self.limits[1]:
                self.value /= o
            else:
                self.value = self.limits[0]
        else:
            self.value /= o
        return self

    def __repr__(self) -> str:
        return str(self.value)


class plane:

    def __init__(self,
                 size,
                 unit_length) -> None:
        """
        params:
        size - (x ,y)
        mode - ('centered', 'x_plus', 'x_negative', 'y_plus', 'y_negative'
                'I', 'II', 'III', 'IV') cartesian quadrants
        unit_length - pixel count for 1 unit length in cartesian system
        """
        self._size = size
        self.unit_length = unit_length
        self._x_dif = self._size[0] // 2
        self._y_dif = self._size[1] // 2
        self.set_limit()

    def __add__(self, o):
        if self.unit_length + o <= self._size[0] or \
                self.unit_length + o <= self._size[1]:
            self.unit_length += o
        return self

    def __sub__(self, o):
        self._x_dif -= o
        self._y_dif -= o
        return self

    def __mul__(self, o):
        if self.unit_length * o <= self._size[0] or \
                self.unit_length * o <= self._size[1]:
            self.unit_length *= o
        return self

    def __truediv__(self, o):
        if self.unit_length // o >= 1:
            self.unit_length //= o
        return self

    @property
    def X(self):
        return self._x_dif

    @X.setter
    def X(self, o):
        if 0 <= o <= self._size[0]:
            self._x_dif = o
        else:
            if o > 0:
                self._x_dif = self._size[0]
            else:
                self._x_dif = 0

    @property
    def Y(self):
        return self._y_dif

    @Y.setter
    def Y(self, o):
        if 0 <= o <= self._size[1]:
            self._y_dif = o
        else:
            if o > 0:
                self._y_dif = self._size[1]
            else:
                self._y_dif = 0

    @property
    def XY(self):
        """(x, y) in pygame coordinate system"""
        return (self.X, self.Y)

    @XY.setter
    def XY(self, pos):
        self.X = pos[0]
        self.Y = pos[1]

    def set_limit(self):
        self.x_lim = [(self._x_dif - self._size[0]) // self.unit_length,
                      (self._size[0] - self._x_dif) // self.unit_length]
        self.y_lim = [(self._y_dif - self._size[1]) // self.unit_length,
                      (self._size[1] - self._y_dif) // self.unit_length]

    def getXY(self, xy):
        ...

    def getX(self, x):
        """Retrun cartesian x in pygame coordinate system"""
        return self._x_dif + x * self.unit_length

    def getY(self, y):
        """Return cartesian y in pygame coordinate system"""
        return self._y_dif - y * self.unit_length

    def toXY(self, center: tuple):
        """Return pygame (x, y) in cartesian coordinate system"""
        return (self.toX(center[0]), self.toY(center[1]))

    def toX(self, x):
        """Return pygame x in cartesian coordinate system"""
        return (x - self._x_dif) / self.unit_length

    def toY(self, y):
        """Return pygame y in cartesian coordinate system"""
        return (self._y_dif - y) / self.unit_length

    def vector(self, x, y):
        """Return vector object parented by current plane object"""
        return vector(x, y, self)


class vector:

    def __init__(self, x, y, space: plane) -> None:
        self.space = space
        self.length_limit = [-math.sqrt(self.space.x_lim[1]**2 +
                                        self.space.y_lim[1]**2),
                             math.sqrt(self.space.x_lim[1]**2 +
                                       self.space.y_lim[1]**2)]
        self._x = scalar(x, self.length_limit)
        self._y = scalar(y, self.length_limit)

    def __add__(self, num):
        if self.length < self.length_limit[1]:
            self._x += num * math.cos(self.direction)
            self._y += num * math.sin(self.direction)
        return self

    def __sub__(self, num):
        # if num > 0 and self.length > self.length_limit[0]:
        if self.length > self.length_limit[0]:
            self._x -= num * math.cos(self.direction)
            self._y -= num * math.sin(self.direction)
        # elif num < 0 and self.length < self.length_limit[1]:
        #     self._x -= num
        #     self._y -= num
        return self

    def __mul__(self, factor):
        """
        Since multiplying by 1 has no effect, ommited factor of 1,
        Ommited negative values. For rotating use rotate method.
        """
        if factor > 1 and self.length < self.length_limit[1]:
            self._x *= factor
            self._y *= factor
        elif 0 <= factor < 1 and self.length > self.length_limit[0]:
            self._x *= factor
            self._y *= factor
        return self

    def __truediv__(self, _):
        """Use multiplication instead"""
        raise Exception("Use multiplication instead :)")

    @property
    def x(self):
        """x coordinate in cartesian system"""
        return self._x.value

    @x.setter
    def x(self, value):
        """set x in cartesian coordinate system"""
        self._x.value = value

    @property
    def y(self):
        """y coordinate in cartesian system"""
        return self._y.value

    @y.setter
    def y(self, value):
        """set y coordinate in cartesian system"""
        self._y.value = value

    @property
    def xy(self):
        """(x, y) values in cartesian coordinate system"""
        return (self.x, self.y)

    @property
    def X(self):
        """X coordinate in pygame system"""
        return self.space.getX(self.x)

    @property
    def Y(self):
        """Y coordinate in pygame system"""
        return self.space.getY(self.y)

    @property
    def XY(self):
        """(x, y) values in pygame coordinate system"""
        return (self.X, self.Y)

    @property
    def length(self):
        """Return length in cartesian coordinate system"""
        return math.sqrt(self.x**2 + self.y**2)

    @property
    def direction(self):
        """Return angle from OX in radians"""
        return math.atan2(self.y, self.x)

    def rotate(self, rad):
        """
        Possitive values for counter-clock-wise,
        negative values for clock-wise rotation
        """
        _x = self.x
        _y = self.y
        self.x = _x * math.cos(rad) - _y * math.sin(rad)
        self.y = _x * math.sin(rad) + _y * math.cos(rad)

    def set_limit(self, max, min):
        self.length_limit = [min, max]
