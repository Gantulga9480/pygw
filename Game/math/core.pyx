import cython
from libc.math cimport cos, sin, atan2, sqrt
from libc.math cimport abs as cabs

pi = 3.141592653589793

cdef class scalar:

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self,
                 double value,
                 (double, double) limits=(0, 0)):
        if limits[0] and limits[1]:
            self.is_limit = True
            self._min = limits[0]
            self._max = limits[1]
            if value < self._min:
                self._num = self._min
            elif value > self._max:
                self._num = self._max
            else:
                self._num = value
        else:
            self.is_limit = False
            self._num = value

    @property
    def value(self):
        return self._num

    @value.setter
    def value(self, o):
        if self.is_limit:
            if (self._min <= o) and (o <= self._max):
                self._num = o
            else:
                self._num = self._min if o < self._min else self._max
        else:
            self._num = o

    def __repr__(self):
        return str(self._num)

    cdef void add(self, double o):
        self.set_value(self._num + o)

    cdef void scale(self, double o):
        self.set_value(self._num * o)

    cdef double get_value(self):
        return self._num

    cdef void set_value(self, double o):
        if self.is_limit:
            if self._min <= o <= self._max:
                self._num = o
            else:
                self._num = self._min if o < self._min else self._max
        else:
            self._num = o


cdef class point2d:

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self,
                 double x,
                 double y,
                 (double, double) x_lim=(0, 0),
                 (double, double) y_lim=(0, 0)):
        self._x = scalar(x, x_lim)
        self._y = scalar(y, y_lim)

    @property
    def x(self):
        return self._x._num

    @x.setter
    def x(self, o):
        self._x.set_value(o)

    @property
    def y(self):
        return self._y._num

    @y.setter
    def y(self, o):
        self._y.set_value(o)

    @property
    def xy(self):
        return (self._x._num, self._y._num)

    @xy.setter
    def xy(self, o):
        self._x.set_value(o[0])
        self._y.set_value(o[1])

    cpdef void set_x_ref(self, scalar o):
        self._x = o

    cpdef void set_y_ref(self, scalar o):
        self._y = o

    cdef void set_x(self, double o):
        self._x.set_value(o)

    cdef double get_x(self):
        return self._x._num

    cdef void set_y(self, double o):
        self._y.set_value(o)

    cdef double get_y(self):
        return self._y._num

    cdef (double, double) get_xy(self):
        return (self._x._num, self._y._num)

    cdef void set_xy(self, (double, double) o):
        self._x.set_value(o[0])
        self._y.set_value(o[1])


cdef class vector2d:

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self,
                 double x,
                 double y,
                 double max_length = 0,
                 double min_length = 0):
        self._head = point2d(x, y)
        self._tail = point2d(0, 0)
        self.max_length = max_length
        self.min_length = min_length
        self.update()

    # TODO add max min check in properties

    @property
    def x(self):
        return self._head._x._num

    @x.setter
    def x(self, o):
        self._head._x.set_value(o)
        self.update()

    @property
    def y(self):
        return self._head._y._num

    @y.setter
    def y(self, o):
        self._head._y.set_value(o)
        self.update()

    @property
    def head(self):
        return (self._head._x._num, self._head._y._num)

    @head.setter
    def head(self, o):
        self._head._x.set_value(o[0])
        self._head._y.set_value(o[1])
        self.update()

    @property
    def tail_x(self):
        return self._tail._x._num

    @tail_x.setter
    def tail_x(self, o):
        self._tail._x.set_value(o)

    @property
    def tail_y(self):
        return self._tail._y._num

    @tail_y.setter
    def tail_y(self, o):
        self._tail._y.set_value(o)

    @property
    def tail(self):
        return (0, 0)

    @tail.setter
    def tail(self, o):
        self._tail._x.set_value(o[0])
        self._tail._y.set_value(o[1])

    def unit(self, double scale=1, bint vector=True):
        cdef double a = self.direction()
        cdef double x = cos(a) * scale
        cdef double y = sin(a) * scale
        if vector:
            return vector2d(x, y, self.max_length, self.min_length)
        return (x, y)

    def normal(self, double scale=1, bint vector=True):
        cdef double x = -(self._head._y._num - self._tail._y._num) * scale
        cdef double y = (self._head._x._num - self._tail._x._num) * scale
        if vector:
            return vector2d(x, y, self.max_length, self.min_length)
        return (x, y)

    cpdef void set_x_ref(self, scalar o):
        self._head._x = o
        self.update()

    cpdef void set_y_ref(self, scalar o):
        self._head._y = o
        self.update()

    cpdef void set_head_ref(self, point2d o):
        self._head = o
        self.update()

    cpdef void set_tail_x_ref(self, scalar o):
        self._tail._x = o

    cpdef void set_tail_y_ref(self, scalar o):
        self._tail._y = o

    cpdef void set_tail_ref(self, point2d o):
        self._tail = o

    cpdef void add(self, double o):
        cdef double a
        cdef (double, double) xy
        if o > 0:
            if self.max_length and ((self.length() + o) <= self.max_length):
                a = self.direction()
                self._head._x.add(o * cos(a))
                self._head._y.add(o * sin(a))
            elif not self.max_length:
                a = self.direction()
                self._head._x.add(o * cos(a))
                self._head._y.add(o * sin(a))
            self.update()
        elif o < 0:
            if cabs(o) < (self.length() - self.min_length):
                a = self.direction()
                self._head._x.add(o * cos(a))
                self._head._y.add(o * sin(a))
            else:
                xy = self.unit(self.min_length, False)
                self._head._x._num = xy[0]
                self._head._y._num = xy[1]
            self.update()

    cpdef void scale(self, double o):
        cdef (double, double) xy
        cdef double v_len = self.length()
        if o > 1:
            if self.max_length:
                if (v_len * o) < self.max_length:
                    self._head._x.scale(o)
                    self._head._y.scale(o)
                else:
                    xy = self.unit(self.max_length, False)
                    self._head._x._num = xy[0]
                    self._head._y._num = xy[1]
            self._head._x.scale(o)
            self._head._y.scale(o)
        elif o < 1:
            if (v_len * o) > self.min_length:
                self._head._x.scale(o)
                self._head._y.scale(o)
            else:
                xy = self.unit(self.min_length, False)
                self._head._x._num = xy[0]
                self._head._y._num = xy[1]
        self.update()

    cpdef void rotate(self, double radians):
        cdef double _x = self._head._x._num
        cdef double _y = self._head._y._num

        self._head._x.set_value(_x * cos(radians) - _y * sin(radians))
        self._head._y.set_value(_x * sin(radians) + _y * cos(radians))
        self.update()

    cpdef double length(self):
        cdef double dx = self._head._x._num - self._tail._x._num
        cdef double dy = self._head._y._num - self._tail._y._num
        return sqrt(dx*dx + dy*dy)

    cpdef double direction(self):
        cdef double dx = self._head._x._num - self._tail._x._num
        cdef double dy = self._head._y._num - self._tail._y._num
        return atan2(dy, dx)

    cpdef double distance_to(self, vector2d vector):
        cdef double dx = self._head._x._num - vector._head._x._num
        cdef double dy = self._head._y._num - vector._head._y._num
        return sqrt(dx*dx + dy*dy)

    cpdef double angle_between(self, vector2d vector):
        return atan2(vector._head._y._num, vector._head._x._num) - self.direction()

    cpdef double dot(self, vector2d vector):
        cdef double x = -(self._head._y._num - self._tail._y._num)
        cdef double y = (self._head._x._num - self._tail._x._num)
        cdef double _x = -(vector._head._y._num - vector._tail._y._num)
        cdef double _y = (vector._head._x._num - vector._tail._x._num)
        return x * _x + y * _y

    cdef void set_x(self, double x):
        self._head._x.set_value(x)
        self.update()

    cdef void set_y(self, double y):
        self._head._y.set_value(y)
        self.update()

    cdef void set_xy(self, (double, double) xy):
        self._head._x.set_value(xy[0])
        self._head._y.set_value(xy[1])
        self.update()

    cdef (double, double) get_xy(self):
        return (self._head._x._num, self._head._y._num)

    cdef void add_xy(self, (double, double) xy):
        cdef (double, double) new_xy
        cdef (double, double) old_xy = self.get_xy()
        self._head._x.add(xy[0])
        self._head._y.add(xy[1])
        if (self.length() > self.max_length):
            # self.set_xy(old_xy)
            new_xy = self.unit(self.max_length, False)
            self._head._x._num = new_xy[0]
            self._head._y._num = new_xy[1]
        self.update()

    cdef (double, double) unit_vector(self, double scale):
        cdef double a = self.direction()
        cdef double x = cos(a) * scale
        cdef double y = sin(a) * scale
        return (x, y)

    cdef (double, double) normal_vector(self, double scale):
        cdef double x = -(self._head._y._num - self._tail._y._num) * scale
        cdef double y = (self._head._x._num - self._tail._x._num) * scale
        return (x, y)

    cdef void update(self):
        ...
