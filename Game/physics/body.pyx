import cython
from Game.graphic.cartesian cimport CartesianPlane, Vector2d
from Game.graphic.shapes cimport Polygon, Rectangle, Triangle
from Game.math.core cimport pi, point2d
from pygame.draw import aalines
from libc.math cimport floor


STATIC = 0
DYNAMIC = 1


@cython.optimize.unpack_method_calls(False)
cdef class object_body:
    def __cinit__(self, *args, **kwargs):
        self.is_attached = False
        self.body_type = STATIC
        self.body_id = 0
        self.radius = 0

    def __init__(self, int body_id, int body_type):
        self.body_id = body_id
        self.body_type = body_type

    cpdef void attach_to(self, object_body o, bint follow_dir):
        if not self.is_attached:
            self.is_attached = True
            self.is_following_dir = follow_dir
            self.parent_body = o
            self.shape.plane.parent_vector.set_head_ref(o.shape.plane.parent_vector.get_head_ref())

    cpdef void detach(self):
        if self.is_attached:
            self.is_attached = False
            self.is_following_dir = False
            self.shape.plane.parent_vector.set_head_ref(point2d(self.parent_body.shape.plane.parent_vector.get_x(), self.parent_body.shape.plane.parent_vector.get_y()))

    cpdef void step(self):
        cdef double d
        if self.is_attached:
            if self.is_following_dir:
                d = self.parent_body.velocity.dir() - self.velocity.dir()
                if d != 0:
                    self.shape.rotate(d)
                    self.velocity.rotate(d)
        self.USR_step()

    cpdef void USR_step(self):
        ...

    cpdef (double, double) position(self):
        return self.shape.plane.parent_vector.get_head()

    cpdef double speed(self):
        return floor((self.velocity.mag() - 1.0) * 10.0) / 10.0

    cpdef void rotate(self, double angle):
        if not self.is_following_dir:
            self.shape.rotate(angle)

    cpdef void scale(self, double factor):
        self.shape.scale(factor)

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.initializedcheck(False)
    def show(self, color=(0, 0, 0), bint show_vertex=False):
        self.shape.plane.parent_vector.update()
        cdef int i
        cdef list heads = []
        if show_vertex:
            for i in range(self.shape.vertex_count):
                (<Vector2d>self.shape.vertices[i]).show(color)
                heads.append((<Vector2d>self.shape.vertices[i]).get_HEAD())
        else:
            for i in range(self.shape.vertex_count):
                heads.append((<Vector2d>self.shape.vertices[i]).get_HEAD())
        aalines(self.shape.window, color, True, heads)

@cython.optimize.unpack_method_calls(False)
cdef class StaticBody(object_body):
    def __cinit__(self, *args, **kwargs):
        pass

    def __init__(self, int body_id, CartesianPlane plane):
        super().__init__(body_id, STATIC)
        self.velocity = Vector2d(plane, 1, 0, 1, 1)
        self.velocity.rotate(pi/2)

@cython.optimize.unpack_method_calls(False)
cdef class DynamicBody(object_body):
    def __cinit__(self, *args, **kwargs):
        pass

    def __init__(self, int body_id, CartesianPlane plane, int max_speed=1):
        super().__init__(body_id, DYNAMIC)
        if plane.parent_vector is None:
            raise AttributeError("A dynamic body can't be made from a base plane, Use child plane instead!")
        self.max_speed = max_speed
        self.velocity = Vector2d(plane, 1, 0, max_speed, 1)
        self.velocity.rotate(pi/2)

    def show(self, color=(0, 0, 0), bint show_vertex=False):
        super().show(color, show_vertex)
        self.velocity.show(color)

    @cython.cdivision(True)
    cpdef void USR_step(self):
        cdef double v_len = floor(self.velocity.mag() * 100.0) / 100.0
        cdef (double, double) xy
        cdef (double, double) _xy
        if v_len > 1:
            if not self.is_attached:
                xy = self.velocity.get_head()
                _xy = self.velocity.unit_vector(1)
                self.shape.plane.parent_vector.set_head((self.shape.plane.parent_vector.get_x() + xy[0] - _xy[0],
                                                         self.shape.plane.parent_vector.get_y() + xy[1] - _xy[1]))
            self.velocity.add(-self.max_speed/120)
        else:
            self.velocity.set_head(self.velocity.unit_vector(1))

    @cython.cdivision(True)
    cpdef void Accelerate(self, double factor):
        if factor == 0:
            self.velocity.add(self.max_speed/60)
        else:
            self.velocity.add(factor)

    cpdef void rotate(self, double angle):
        self.shape.rotate(angle)
        self.velocity.rotate(angle)

@cython.optimize.unpack_method_calls(False)
cdef class DynamicPolygonBody(DynamicBody):
    def __cinit__(self, *args, **kwargs):
        pass

    def __init__(self, int body_id, CartesianPlane plane, tuple size, int max_speed=1):
        super().__init__(body_id, plane, max_speed)
        self.radius = max(size)
        self.shape = Polygon(plane, size)

@cython.optimize.unpack_method_calls(False)
cdef class DynamicRectangleBody(DynamicBody):
    def __cinit__(self, *args, **kwargs):
        pass

    def __init__(self, int body_id, CartesianPlane plane, tuple size, int max_speed=1):
        super().__init__(body_id, plane, max_speed)
        self.radius = max(size)
        self.shape = Rectangle(plane, size)

@cython.optimize.unpack_method_calls(False)
cdef class DynamicTriangleBody(DynamicBody):
    def __cinit__(self, *args, **kwargs):
        pass

    def __init__(self, int body_id, CartesianPlane plane, tuple size, int max_speed=1):
        super().__init__(body_id, plane, max_speed)
        self.radius = max(size)
        self.shape = Triangle(plane, size)

cdef class StaticPolygonBody(StaticBody):
    def __cinit__(self, *args, **kwargs):
        pass

    def __init__(self, int body_id, CartesianPlane plane, tuple size):
        super().__init__(body_id, plane)
        self.radius = max(size)
        self.shape = Polygon(plane, size)

cdef class StaticRectangleBody(StaticBody):
    def __cinit__(self, *args, **kwargs):
        pass

    def __init__(self, int body_id, CartesianPlane plane, tuple size):
        super().__init__(body_id, plane)
        self.radius = max(size)
        self.shape = Rectangle(plane, size)

cdef class StaticTriangleBody(StaticBody):
    def __cinit__(self, *args, **kwargs):
        pass

    def __init__(self, int body_id, CartesianPlane plane, tuple size):
        super().__init__(body_id, plane)
        self.radius = max(size)
        self.shape = Triangle(plane, size)