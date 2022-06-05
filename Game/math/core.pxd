cdef double pi

cdef class scalar:
    cdef readonly bint is_limit
    cdef double _min, _max, num

    cdef void add(self, double o)
    cdef void scale(self, double o)
    cdef double get(self)
    cdef void set(self, double o)

cdef class point2d:
    cdef scalar x, y

    cpdef void set_x_ref(self, scalar o)
    cpdef void set_y_ref(self, scalar o)
    cdef void set_x(self, double o)
    cdef void set_y(self, double o)
    cdef double get_x(self)
    cdef double get_y(self)
    cdef (double, double) get_xy(self)
    cdef void set_xy(self, (double, double) o)

cdef class vector2d:
    cdef point2d head, tail
    cdef double max_length, min_length

    cpdef void add(self, double o)
    cpdef void scale(self, double o)
    cpdef void set_head_ref(self, point2d o)
    cpdef void set_tail_ref(self, point2d o)
    cpdef void rotate(self, double radians)
    cpdef double mag(self)
    cpdef double dir(self)
    cpdef double distance_to(self, vector2d vector)
    cpdef double angle_between(self, vector2d vector)
    cpdef double dot(self, vector2d vector)
    cdef void update(self)
    cdef void set_x(self, double x)
    cdef void set_y(self, double y)
    cdef void set_xy(self, (double, double) xy)
    cdef (double, double) get_xy(self)
    cdef void add_xy(self, (double, double) xy)
    cdef (double, double) unit_vector(self, double scale)
    cdef (double, double) normal_vector(self, double scale)
