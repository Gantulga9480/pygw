import cython
from libc.math cimport cos, sin, atan2, sqrt
from libc.math cimport abs as cabs

pi = 3.141592653589793

@cython.optimize.unpack_method_calls(False)
@cython.nonecheck(False)
cdef class scalar:

    def __cinit__(self, *args, **kwargs):
        self.num = 0
        self.min = 0
        self.max = 0
        self._clamped = False

    def __init__(self, double value, (double, double) limits=(0, 0)):
        if limits[0] or limits[1]:
            self.min = limits[0]
            self.max = limits[1]
            self._clamped = True
            if value < self.min:
                self.num = self.min
            elif value > self.max:
                self.num = self.max
            else:
                self.num = value
        else:
            self.num = value
            self._clamped = False

    @property
    def value(self):
        return self.num

    @value.setter
    def value(self, double o):
        if self._clamped:
            if self.min <= o <= self.max:
                self.num = o
            else:
                self.num = self.min if o < self.min else self.max
        else:
            self.num = o

    def __repr__(self):
        return str(self.num)

    cdef void add(self, double o):
        self.set_value(self.num + o)

    cdef void scale(self, double o):
        self.set_value(self.num * o)

    cdef double get_value(self):
        return self.num

    cdef void set_value(self, double o):
        if self._clamped:
            if self.min <= o <= self.max:
                self.num = o
            else:
                self.num = self.min if o < self.min else self.max
        else:
            self.num = o


@cython.optimize.unpack_method_calls(False)
@cython.nonecheck(False)
cdef class point2d:

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self, double x, double y, (double, double) x_lim=(0, 0), (double, double) y_lim=(0, 0)):
        self._x = scalar(x, x_lim)
        self._y = scalar(y, y_lim)

    @property
    def x(self):
        return self._x.num

    @x.setter
    def x(self, double o):
        self._x.set_value(o)

    @property
    def y(self):
        return self._y.num

    @y.setter
    def y(self, double o):
        self._y.set_value(o)

    @property
    def xy(self):
        return (self._x.num, self._y.num)

    @xy.setter
    def xy(self, (double, double) o):
        self._x.set_value(o[0])
        self._y.set_value(o[1])

    cpdef void set_x_ref(self, scalar o):
        self._x = o

    cpdef void set_y_ref(self, scalar o):
        self._y = o

    cpdef scalar get_x_ref(self):
        return self._x

    cpdef scalar get_y_ref(self):
        return self._y

    cdef void set_x(self, double o):
        self._x.set_value(o)

    cdef double get_x(self):
        return self._x.num

    cdef void set_y(self, double o):
        self._y.set_value(o)

    cdef double get_y(self):
        return self._y.num

    cdef (double, double) get_xy(self):
        return (self._x.num, self._y.num)

    cdef void set_xy(self, (double, double) o):
        self._x.set_value(o[0])
        self._y.set_value(o[1])


@cython.optimize.unpack_method_calls(False)
@cython.nonecheck(False)
cdef class vector2d:

    def __cinit__(self, *args, **kwargs):
        self.max = 0
        self.min = 0

    def __init__(self, double x, double y, double max = 0, double min = 0):
        self._head = point2d(x, y)
        self.max = max
        self.min = min

    @property
    def x(self):
        return self._head._x.num

    @x.setter
    def x(self, double o):
        cdef double _len
        cdef double angle
        _len = sqrt(o * o + self._head._y.num * self._head._y.num)
        if _len >= self.min:
            if self.max:
                if _len <= self.max:
                    self._head._x.set_value(o)
                else:
                    angle = self.dir()
                    self._head._x.set_value(cos(angle) * self.max)
            else:
                self._head._x.set_value(o)
        else:
            angle = self.dir()
            self._head._x.set_value(cos(angle) * self.min)

    @property
    def y(self):
        return self._head._y.num

    @y.setter
    def y(self, double o):
        cdef double _len
        cdef double angle
        _len = sqrt(o * o + self._head._x.num * self._head._x.num)
        if _len >= self.min:
            if self.max:
                if _len <= self.max:
                    self._head._y.set_value(o)
                else:
                    angle = self.dir()
                    self._head._y.set_value(sin(angle) * self.max)
            else:
                self._head._y.set_value(o)
        else:
            angle = self.dir()
            self._head._y.set_value(sin(angle) * self.min)

    @property
    def head(self):
        return (self._head._x.num, self._head._y.num)

    @head.setter
    def head(self, (double, double) o):
        cdef double _len
        cdef double angle
        _len = sqrt(o[0]*o[0] + o[1]*o[1])
        if _len >= self.min:
            if self.max:
                if _len <= self.max:
                    self._head._x.set_value(o[0])
                    self._head._y.set_value(o[1])
                else:
                    angle = self.dir()
                    self._head._x.set_value(cos(angle) * self.max)
                    self._head._y.set_value(sin(angle) * self.max)
            else:
                self._head._x.set_value(o[0])
                self._head._y.set_value(o[1])
        else:
            angle = self.dir()
            self._head._x.set_value(cos(angle) * self.min)
            self._head._y.set_value(sin(angle) * self.min)

    def unit(self, double scale=1, bint vector=True):
        cdef double a = self.dir()
        cdef double x = cos(a) * scale
        cdef double y = sin(a) * scale
        if vector:
            return vector2d(x, y, self.max, self.min)
        return (x, y)

    def normal(self, double scale=1, bint vector=True):
        cdef double x = -self._head._y.num * scale
        cdef double y = self._head._x.num * scale
        if vector:
            return vector2d(x, y, self.max, self.min)
        return (x, y)

    cpdef void set_x_ref(self, scalar o):
        self._head._x = o

    cpdef void set_y_ref(self, scalar o):
        self._head._y = o

    cpdef void set_head_ref(self, point2d o):
        cdef double _len = sqrt(o._x.num*o._x.num + o._y.num*o._y.num)
        if _len >= self.min:
            if self.max:
                if _len <= self.max:
                    self._head = o
            else:
                self._head = o

    cpdef scalar get_x_ref(self):
        return self._head.get_x_ref()

    cpdef scalar get_y_ref(self):
        return self._head.get_y_ref()

    cpdef point2d get_head_ref(self):
        return self._head

    cpdef void add(self, double o):
        cdef double a = self.dir()
        if o > 0:
            if self.max:
                if (self.mag() + o) <= self.max:
                    self._head._x.add(o * cos(a))
                    self._head._y.add(o * sin(a))
                else:
                    self._head._x.num = cos(a) * self.max
                    self._head._y.num = sin(a) * self.max
            else:
                self._head._x.add(o * cos(a))
                self._head._y.add(o * sin(a))
        elif o < 0:
            if cabs(o) < (self.mag() - self.min):
                self._head._x.add(o * cos(a))
                self._head._y.add(o * sin(a))
            else:
                self._head._x.num = cos(a) * self.min
                self._head._y.num = sin(a) * self.min

    cpdef void scale(self, double o):
        cdef double angle
        if o > 1:
            if self.max:
                if (self.mag() * o) < self.max:
                    self._head._x.scale(o)
                    self._head._y.scale(o)
                else:
                    angle = self.dir()
                    self._head._x.num = cos(angle) * self.max
                    self._head._y.num = sin(angle) * self.max
            else:
                self._head._x.scale(o)
                self._head._y.scale(o)
        elif 0 <= o < 1:
            if (self.mag() * o) > self.min:
                self._head._x.scale(o)
                self._head._y.scale(o)
            else:
                angle = self.dir()
                self._head._x.num = cos(angle) * self.min
                self._head._y.num = sin(angle) * self.min

    cpdef void rotate(self, double radians):
        cdef double x = self._head._x.num
        cdef double y = self._head._y.num
        self._head._x.set_value(x * cos(radians) - y * sin(radians))
        self._head._y.set_value(x * sin(radians) + y * cos(radians))

    cpdef double mag(self):
        return sqrt(self._head._x.num*self._head._x.num + self._head._y.num*self._head._y.num)

    cpdef double dir(self):
        return atan2(self._head._y.num, self._head._x.num)

    cpdef double dist(self, vector2d vector):
        cdef double dx = self._head._x.num - vector._head._x.num
        cdef double dy = self._head._y.num - vector._head._y.num
        return sqrt(dx*dx + dy*dy)

    cpdef double angle_between(self, vector2d vector):
        return atan2(vector._head._y.num, vector._head._x.num) - self.dir()

    cpdef double dot(self, vector2d vector):
        return self._head._x.num * vector._head._x.num + self._head._y.num * vector._head._y.num

    cdef void set_x(self, double o):
        cdef double _len
        cdef double angle
        _len = sqrt(o * o + self._head._y.num * self._head._y.num)
        if _len >= self.min:
            if self.max:
                if _len <= self.max:
                    self._head._x.set_value(o)
                else:
                    angle = self.dir()
                    self._head._x.set_value(cos(angle) * self.max)
            else:
                self._head._x.set_value(o)
        else:
            angle = self.dir()
            self._head._x.set_value(cos(angle) * self.min)

    cdef void set_y(self, double o):
        cdef double _len
        cdef double angle
        _len = sqrt(o * o + self._head._x.num * self._head._x.num)
        if _len >= self.min:
            if self.max:
                if _len <= self.max:
                    self._head._y.set_value(o)
                else:
                    angle = self.dir()
                    self._head._y.set_value(sin(angle) * self.max)
            else:
                self._head._y.set_value(o)
        else:
            angle = self.dir()
            self._head._y.set_value(sin(angle) * self.min)

    cdef void set_head(self, (double, double) o):
        cdef double _len = sqrt(o[0]*o[0] + o[1]*o[1])
        cdef double angle
        if _len >= self.min:
            if self.max:
                if _len <= self.max:
                    self._head._x.set_value(o[0])
                    self._head._y.set_value(o[1])
                else:
                    angle = self.dir()
                    self._head._x.set_value(cos(angle) * self.max)
                    self._head._y.set_value(sin(angle) * self.max)
            else:
                self._head._x.set_value(o[0])
                self._head._y.set_value(o[1])
        else:
            angle = self.dir()
            self._head._x.set_value(cos(angle) * self.min)
            self._head._y.set_value(sin(angle) * self.min)

    cdef double get_x(self):
        return self._head._x.num

    cdef double get_y(self):
        return self._head._y.num

    cdef (double, double) get_head(self):
        return (self._head.get_x(), self._head.get_y())

    cdef (double, double) unit_vector(self, double scale):
        cdef double a = self.dir()
        cdef double x = cos(a) * scale
        cdef double y = sin(a) * scale
        return (x, y)

    cdef (double, double) normal_vector(self, double scale):
        cdef double x = -self._head._y.num * scale
        cdef double y = self._head._x.num * scale
        return (x, y)
