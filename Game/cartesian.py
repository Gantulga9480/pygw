import math


class scalar:

    def __init__(self, value=0, limits=None) -> None:
        self.value = value
        self.limits = limits

    def __add__(self, o: object):
        if self.limits and self.value + o <= self.limits[1]:
            self.value += o
        return self

    def __sub__(self, o: object):
        if self.limits and self.value - o >= self.limits[0]:
            self.value -= o
        return self

    def __mul__(self, o: object):
        self.value *= o
        return self

    def __truediv__(self, o: object):
        self.value /= o
        return self

    def __repr__(self) -> str:
        return str(self.value)


class plane:

    def __init__(self,
                 screen_size,
                 mode,
                 space) -> None:
        """
        params:
        screen_size - (x ,y)
        mode - ('centered', 'x_plus', 'x_negative', 'y_plus', 'y_negative'
                'I', 'II', 'III', 'IV') cartesian quadrants
        space - pixel count for 1 unit length in cartesian system
        """
        self._size = screen_size
        self.mode = mode
        self.space = space
        self._x_dif, self._y_dif = 0, 0
        self.x_lim, self.y_lim = 0, 0
        if self.mode == 'center':
            self._x_dif = self._size[0] // 2
            self._y_dif = self._size[1] // 2
            self.x_lim = [(self._x_dif - self._size[0]) // self.space,
                          (self._size[0] - self._x_dif) // self.space]
            self.y_lim = [(self._y_dif - self._size[1]) // self.space,
                          (self._size[1] - self._y_dif) // self.space]
        elif self.mode == 'x+':
            self._y_dif = self._size[1] // 2
            self.x_lim = [0,
                          (self._size[0] - self._x_dif) // self.space]
            self.y_lim = [(self._y_dif - self._size[1]) // self.space,
                          (self._size[1] - self._y_dif) // self.space]
        elif self.mode == 'x-':
            self._x_dif = self._size[0]
            self._y_dif = self._size[1] // 2
            self.x_lim = [(self._x_dif - self._size[0]) // self.space,
                          0]
            self.y_lim = [(self._y_dif - self._size[1]) // self.space,
                          (self._size[1] - self._y_dif) // self.space]
        elif self.mode == 'y+':
            self._x_dif = self._size[0] // 2
            self._y_dif = self._size[1]
            self.x_lim = [(self._x_dif - self._size[0]) // self.space,
                          (self._size[0] - self._x_dif) // self.space]
            self.y_lim = [0,
                          (self._size[1] - self._y_dif) // self.space]
        elif self.mode == 'y-':
            self._x_dif = self._size[0] // 2
            self.x_lim = [(self._x_dif - self._size[0]) // self.space,
                          (self._size[0] - self._x_dif) // self.space]
            self.y_lim = [(self._y_dif - self._size[1]) // self.space,
                          0]
        elif self.mode == 'I':
            self._y_dif = self._size[1]
            self.x_lim = [0,
                          (self._size[0] - self._x_dif) // self.space]
            self.y_lim = [0,
                          (self._size[1] - self._y_dif) // self.space]
        elif self.mode == 'II':
            self._x_dif = self._size[0]
            self._y_dif = self._size[1]
            self.x_lim = [(self._x_dif - self._size[0]) // self.space,
                          0]
            self.y_lim = [0,
                          (self._size[1] - self._y_dif) // self.space]
        elif self.mode == 'III':
            self._x_dif = self._size[0]
            self.x_lim = [(self._x_dif - self._size[0]) // self.space,
                          0]
            self.y_lim = [(self._y_dif - self._size[1]) // self.space,
                          0]
        elif self.mode == 'IV':
            self.x_lim = [0,
                          (self._size[0] - self._x_dif) // self.space]
            self.y_lim = [(self._y_dif - self._size[1]) // self.space,
                          0]
        else:
            raise ValueError('Unsupported mode!')

    @property
    def center(self):
        return (self._x_dif, self._y_dif)

    def getX(self, x=None):
        """Return real x coordinate in pygame coordinate system"""
        if x is not None:
            return self._x_dif + x * self.space
        return self._x_dif

    def getY(self, y=None):
        """Return real y coordinate in pygame coordinate system"""
        if y is not None:
            return self._y_dif - y * self.space
        return self._y_dif

    def toX(self, x):
        """Return real x coordinate in cartesian system"""
        return (x - self._x_dif) / self.space

    def toY(self, y):
        """Return real y coordinate in cartesian system"""
        return (self._y_dif - y) / self.space


class vector:

    def __init__(self) -> None:
        self.space: plane = None
        self.x: scalar = None
        self.y: scalar = None

    @property
    def length(self):
        return math.sqrt(self.x.value**2 + self.y.value**2)

    @property
    def direction(self):
        return math.atan2(self.y.value, self.x.value)

    def scale(self, factor):
        self.x *= factor
        self.y *= factor

    def rotate(self, rad):
        _x = self.x.value
        _y = self.y.value
        self.x.value = _x * math.cos(rad) - _y * math.sin(rad)
        self.y.value = _x * math.sin(rad) + _y * math.cos(rad)


class CartesianPlane(plane):

    def __init__(self,
                 screen_size: tuple,
                 mode: str = 'center',
                 space=10) -> None:
        super().__init__(screen_size, mode, space)

    def move_with(self, vec: vector):
        if vec.length > 0:
            if 0 <= self._x_dif + vec.x.value <= self._size[0]:
                self._x_dif += vec.x.value
            else:
                if vec.x.value > 0:
                    self._x_dif = self._size[0]
                else:
                    self._x_dif = 0
            if 0 <= self._y_dif - vec.y.value <= self._size[1]:
                self._y_dif -= vec.y.value
            else:
                if vec.y.value > 0:
                    self._y_dif = 0
                else:
                    self._y_dif = self._size[1]

    def move(self, x, y):
        self._x_dif += x
        self._y_dif -= y


class Vector2D(vector):

    def __init__(self, x, y, space: plane) -> None:
        super().__init__()
        self.space = space
        self.x = scalar(x, self.space.x_lim)
        self.y = scalar(y, self.space.y_lim)

    @property
    def X(self):
        return self.space.getX(self.x.value)

    @property
    def Y(self):
        return self.space.getY(self.y.value)

    @property
    def XY(self):
        return (self.X, self.Y)
