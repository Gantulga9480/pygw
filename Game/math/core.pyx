import cython
from libc.math cimport cos, sin, atan2, sqrt
from libc.math cimport abs as cabs

pi = 3.141592653589793

@cython.optimize.unpack_method_calls(False)
@cython.nonecheck(False)
cdef class scalar:

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self,
                 double value,
                 (double, double) limits=(0, 0)):
        if limits[0] or limits[1]:
            self.is_limit = True
            self._min = limits[0]
            self._max = limits[1]
            if value < self._min:
                self.num = self._min
            elif value > self._max:
                self.num = self._max
            else:
                self.num = value
        else:
            self.is_limit = False
            self.num = value

    @property
    def value(self):
        return self.num

    @value.setter
    def value(self, double o):
        if self.is_limit:
            if (self._min <= o) and (o <= self._max):
                self.num = o
            else:
                self.num = self._min if o < self._min else self._max
        else:
            self.num = o

    def __repr__(self):
        return str(self.num)

    cdef void add(self, double o):
        self.set(self.num + o)

    cdef void scale(self, double o):
        self.set(self.num * o)

    cdef double get(self):
        return self.num

    cdef void set(self, double o):
        if self.is_limit:
            if self._min <= o <= self._max:
                self.num = o
            else:
                self.num = self._min if o < self._min else self._max
        else:
            self.num = o


@cython.optimize.unpack_method_calls(False)
@cython.nonecheck(False)
cdef class point2d:

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self,
                 x,
                 y,
                 x_lim=(0, 0),
                 y_lim=(0, 0)):
        self.x = scalar(x, x_lim)
        self.y = scalar(y, y_lim)

    @property
    def x(self):
        return self.x.num

    @x.setter
    def x(self, double o):
        self.x.set(o)

    @property
    def y(self):
        return self.y.num

    @y.setter
    def y(self, double o):
        self.y.set(o)

    @property
    def xy(self):
        return (self.x.num, self.y.num)

    @xy.setter
    def xy(self, (double, double) o):
        self.x.set(o[0])
        self.y.set(o[1])

    cpdef void set_x_ref(self, scalar o):
        self.x = o

    cpdef void set_y_ref(self, scalar o):
        self.y = o

    cdef void set_x(self, double o):
        self.x.set(o)

    cdef double get_x(self):
        return self.x.num

    cdef void set_y(self, double o):
        self.y.set(o)

    cdef double get_y(self):
        return self.y.num

    cdef (double, double) get_xy(self):
        return (self.x.num, self.y.num)

    cdef void set_xy(self, (double, double) o):
        self.x.set(o[0])
        self.y.set(o[1])


@cython.optimize.unpack_method_calls(False)
@cython.nonecheck(False)
cdef class vector2d:

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self,
                 x,
                 y,
                 double max_length = 0,
                 double min_length = 0):
        self.head = point2d(x, y)
        self.tail = point2d(0, 0)
        self.max_length = max_length
        self.min_length = min_length
        self.update()

    @property
    def x(self):
        return self.head.x.num

    @x.setter
    def x(self, double o):
        # BUG check min max
        # self.head.x.set(o)
        # self.update()
        raise NotImplementedError

    @property
    def y(self):
        return self.head.y.num

    @y.setter
    def y(self, double o):
        # BUG check min max
        # self.head.y.set(o)
        # self.update()
        raise NotImplementedError

    @property
    def head(self):
        return (self.head.x.num, self.head.y.num)

    @head.setter
    def head(self, (double, double) o):
        # BUG check min max
        # self.head.x.set(o[0])
        # self.head.y.set(o[1])
        # self.update()
        raise NotImplementedError

    @property
    def tail_x(self):
        return self.tail.x.num

    @tail_x.setter
    def tail_x(self, double o):
        # BUG check min max
        # self.tail.x.set(o)
        raise NotImplementedError

    @property
    def tail_y(self):
        return self.tail.y.num

    @tail_y.setter
    def tail_y(self, double o):
        # BUG check min max
        # self.tail.y.set(o)
        raise NotImplementedError

    @property
    def tail(self):
        return (self.tail.x.num, self.tail.y.num)

    @tail.setter
    def tail(self, (double, double) o):
        # BUG check min max
        # self.tail.x.set(o[0])
        # self.tail.y.set(o[1])
        raise NotImplementedError

    def unit(self, double scale=1, bint vector=True):
        cdef double a = self.dir()
        cdef double x = cos(a) * scale
        cdef double y = sin(a) * scale
        if vector:
            return vector2d(x, y, self.max_length, self.min_length)
        return (x, y)

    def normal(self, double scale=1, bint vector=True):
        cdef double x = -(self.head.y.num - self.tail.y.num) * scale
        cdef double y = (self.head.x.num - self.tail.x.num) * scale
        if vector:
            return vector2d(x, y, self.max_length, self.min_length)
        return (x, y)

    cpdef void set_head_ref(self, point2d o):
        # BUG decide later for more bug free code
        # self.head = o
        # self.update()
        raise NotImplementedError

    cpdef void set_tail_ref(self, point2d o):
        # BUG decide later for more bug free code
        # self.tail = o
        raise NotImplementedError

    cpdef void add(self, double o):
        cdef double a
        cdef (double, double) xy
        if o > 0:
            if self.max_length:
                if (self.mag() + o) <= self.max_length:
                    a = self.dir()
                    self.head.x.add(o * cos(a))
                    self.head.y.add(o * sin(a))
                else:
                    xy = self.unit_vector(self.max_length)
                    self.head.x.num = xy[0]
                    self.head.y.num = xy[1]
            else:
                a = self.dir()
                self.head.x.add(o * cos(a))
                self.head.y.add(o * sin(a))
        elif o < 0:
            if cabs(o) < (self.mag() - self.min_length):
                a = self.dir()
                self.head.x.add(o * cos(a))
                self.head.y.add(o * sin(a))
            else:
                xy = self.unit_vector(self.min_length)
                self.head.x.num = xy[0]
                self.head.y.num = xy[1]
        self.update()

    cpdef void scale(self, double o):
        cdef (double, double) xy
        cdef double v_len = self.mag()
        if o > 1:
            if self.max_length:
                if (v_len * o) < self.max_length:
                    self.head.x.scale(o)
                    self.head.y.scale(o)
                else:
                    xy = self.unit_vector(self.max_length)
                    self.head.x.num = xy[0]
                    self.head.y.num = xy[1]
            else:
                self.head.x.scale(o)
                self.head.y.scale(o)
        elif o < 1:
            if (v_len * o) > self.min_length:
                self.head.x.scale(o)
                self.head.y.scale(o)
            else:
                xy = self.unit_vector(self.min_length)
                self.head.x.num = xy[0]
                self.head.y.num = xy[1]
        self.update()

    cpdef void rotate(self, double radians):
        cdef double x = self.head.x.num
        cdef double y = self.head.y.num
        self.head.x.set(x * cos(radians) - y * sin(radians))
        self.head.y.set(x * sin(radians) + y * cos(radians))
        self.update()

    cpdef double mag(self):
        cdef double dx = self.head.x.num - self.tail.x.num
        cdef double dy = self.head.y.num - self.tail.y.num
        return sqrt(dx*dx + dy*dy)

    cpdef double dir(self):
        cdef double dx = self.head.x.num - self.tail.x.num
        cdef double dy = self.head.y.num - self.tail.y.num
        return atan2(dy, dx)

    cpdef double distance_to(self, vector2d vector):
        cdef double dx = self.head.x.num - vector.head.x.num
        cdef double dy = self.head.y.num - vector.head.y.num
        return sqrt(dx*dx + dy*dy)

    cpdef double angle_between(self, vector2d vector):
        return atan2(vector.head.y.num, vector.head.x.num) - self.dir()

    cpdef double dot(self, vector2d vector):
        cdef double x = -(self.head.y.num - self.tail.y.num)
        cdef double y = (self.head.x.num - self.tail.x.num)
        cdef double _x = -(vector.head.y.num - vector.tail.y.num)
        cdef double _y = (vector.head.x.num - vector.tail.x.num)
        return x * _x + y * _y

    cdef void set_x(self, double x):
        # BUG check min max
        # self.head.x.set(x)
        # self.update()
        raise NotImplementedError

    cdef void set_y(self, double y):
        # BUG check min max
        # self.head.y.set(y)
        # self.update()
        raise NotImplementedError

    cdef void set_xy(self, (double, double) xy):
        cdef double _len = sqrt(xy[0]*xy[0] + xy[1]*xy[1])
        if self.min_length <= _len <= self.max_length:
            self.head.x.set(xy[0])
            self.head.y.set(xy[1])
            self.update()

    cdef (double, double) get_xy(self):
        return (self.head.x.num, self.head.y.num)

    cdef void add_xy(self, (double, double) xy):
        cdef (double, double) new_xy
        self.head.x.add(xy[0])
        self.head.y.add(xy[1])
        if self.max_length:
            if (self.mag() > self.max_length):
                new_xy = self.unit_vector(self.max_length)
                self.head.x.num = new_xy[0]
                self.head.y.num = new_xy[1]
        self.update()

    cdef (double, double) unit_vector(self, double scale):
        cdef double a = self.dir()
        cdef double x = cos(a) * scale
        cdef double y = sin(a) * scale
        return (x, y)

    cdef (double, double) normal_vector(self, double scale):
        cdef double x = -(self.head.y.num - self.tail.y.num) * scale
        cdef double y = (self.head.x.num - self.tail.x.num) * scale
        return (x, y)

    cdef void update(self):
        ...