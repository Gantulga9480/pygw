from Game.math.core cimport point2d, vector2d


cdef class CartesianPlane:
    cdef object window
    cdef (double, double) window_size
    cdef double unit_length
    cdef readonly Vector2d parent_vector
    cdef point2d center
    cdef double x_min
    cdef double y_min
    cdef double x_max
    cdef double y_max

    cpdef object get_window(self)
    cpdef (double, double) get_window_size(self)
    cpdef double get_unit_length(self)
    cpdef double to_X(self, double x)
    cpdef double to_Y(self, double y)
    cpdef (double, double) to_XY(self, (double, double) xy)
    cpdef double to_x(self, double X)
    cpdef double to_y(self, double Y)
    cpdef (double, double) to_xy(self, (double, double) XY)
    cdef (double, double) get_CENTER(self)
    cdef double get_X(self)
    cdef double get_Y(self)
    cdef void set_limit(self)


cdef class Vector2d(vector2d):

    cdef object window
    cdef CartesianPlane plane
    cdef point2d headXY

    cpdef void random(self)
    cdef double get_X(self)
    cdef double get_Y(self)
    cdef (double, double) get_HEAD(self)
    cdef (double, double) get_TAIL(self)
