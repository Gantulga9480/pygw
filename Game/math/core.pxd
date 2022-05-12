cdef double pi

cdef class scalar:
    cdef readonly bint is_limit
    cdef double _min, _max, _num

    cdef void add(self, double o)
    cdef void scale(self, double o)
    cdef double get_value(self)
    cdef void set_value(self, double o)

cdef class point2d:
    cdef scalar _x, _y

    cpdef void set_x_ref(self, scalar o)
    cpdef void set_y_ref(self, scalar o)
    cdef void set_x(self, double o)
    cdef void set_y(self, double o)
    cdef double get_x(self)
    cdef double get_y(self)
    cdef (double, double) get_xy(self)
    cdef void set_xy(self, (double, double) o)

cdef class vector2d:
    cdef point2d _head, _tail
    cdef (double, double) x_lim
    cdef (double, double) y_lim
    cdef double max_length, min_length

    cpdef void add(self, double o)
    cpdef void scale(self, double o)
    cpdef void set_x_ref(self, scalar o)
    cpdef void set_y_ref(self, scalar o)
    cpdef void set_head_ref(self, point2d o)
    cpdef void set_tail_x_ref(self, scalar o)
    cpdef void set_tail_y_ref(self, scalar o)
    cpdef void set_tail_ref(self, point2d o)
    cpdef void rotate(self, double radians)
    cpdef double length(self)
    cpdef double direction(self)
    cpdef double distance_to(self, vector2d vector)
    cpdef double angle_between(self, vector2d vector)
    cpdef double dot(self, vector2d vector)
    cpdef void update(self)
