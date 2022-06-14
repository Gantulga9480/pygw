from Game.math.core cimport point2d, vector2d


cdef class CartesianPlane:
    cdef public object window
    cdef public (double, double) window_size
    cdef public double unit_length
    cdef public Vector2d parent_vector
    cdef public point2d center
    cdef public double x_min, y_min, x_max, y_max

    cpdef Vector2d get_parent_vector(self)
    cpdef point2d get_center_point(self)
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
