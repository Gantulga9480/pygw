import cython
from Game.graphic.cartesian cimport CartesianPlane, Vector2d
from Game.graphic.shapes cimport Polygon, Rectangle, Triangle, Line
from Game.math.core cimport pi, point2d
from pygame.draw import aalines
from libc.math cimport floor
import numpy as np


STATIC = 0
DYNAMIC = 1
FREE = 2


@cython.optimize.unpack_method_calls(False)
cdef class object_body:
    def __cinit__(self, *args, **kwargs):
        self.is_attached = False
        self.is_following_dir = False
        self.type = FREE
        self.id = 0
        self.radius = 0
        self.friction_factor = 0.3
        self.parent_body = None

    def __init__(self, int id, int type, int vertex_count):
        self.id = id
        self.type = type
        self.collision_point = np.array([point2d(0, 0) for _ in range(vertex_count)], dtype=point2d)

    cpdef void attach(self, object_body o, bint follow_dir):
        if not o.is_attached:
            o.is_attached = True
            o.is_following_dir = follow_dir
            o.parent_body = self
            o.shape.plane.parent_vector.set_head_ref(self.shape.plane.parent_vector.get_head_ref())

    cpdef void detach(self, object_body o):
        if o.is_attached and o.parent_body is self:
            o.is_attached = False
            o.is_following_dir = False
            self.shape.plane.parent_vector.set_head_ref(point2d(self.shape.plane.parent_vector.get_x(), self.shape.plane.parent_vector.get_y()))

    cpdef void step(self):
        cdef double d
        if self.is_attached and self.is_following_dir:
            d = self.parent_body.velocity.dir() - self.velocity.dir()
            if d != 0:
                self.shape.rotate(d)
                self.velocity.rotate(d)
        self.USR_step()

    cpdef void USR_step(self):
        pass

    cpdef void USR_resolve_collision(self, object_body o, (double, double) dxy):
        pass

    cpdef void rotate(self, double angle):
        if not self.is_following_dir:
            self.shape.rotate(angle)

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.initializedcheck(False)
    cpdef void scale(self, double factor):
        cdef int i
        cdef double v_len
        cdef double _min = (<Vector2d>self.shape.vertices[0]).mag()
        for i in range(self.shape.vertex_count):
            v_len = (<Vector2d>self.shape.vertices[i]).mag()
            if v_len < _min:
                _min = v_len
        if factor > 1:
            for i in range(self.shape.vertex_count):
                (<Vector2d>self.shape.vertices[i]).scale(factor)
            self.radius *= factor
        elif factor < 1:
            if _min * factor >= self.shape.vertices[0].min_length:
                for i in range(self.shape.vertex_count):
                    (<Vector2d>self.shape.vertices[i]).scale(factor)
                self.radius *= factor

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

    cpdef (double, double) position(self):
        return self.shape.plane.parent_vector.get_head()

    cpdef double speed(self):
        return floor((self.velocity.mag() - 1.0) * 10.0) / 10.0

@cython.optimize.unpack_method_calls(False)
cdef class FreeBody(object_body):
    def __cinit__(self, *args, **kwargs):
        pass

    def __init__(self, int id, CartesianPlane plane, int vertex_count):
        if plane.parent_vector is None:
            raise AttributeError("A body can't be made from a base plane, Use child plane instead!")
        super().__init__(id, FREE, vertex_count)
        self.velocity = Vector2d(plane, 1, 0, 0, 1)
        self.velocity.rotate(pi/2)

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
        else:
            self.velocity.set_head(self.velocity.unit_vector(1))

    cpdef void Accelerate(self, double factor):
        if factor == 0:
            self.velocity.add(0.1)
        else:
            self.velocity.add(factor)

    cpdef void rotate(self, double angle):
        if not self.is_following_dir:
            self.shape.rotate(angle)
            self.velocity.rotate(angle)

    def show(self, color=(0, 0, 0), bint show_vertex=False):
        super().show(color, show_vertex)
        self.velocity.show(color)

@cython.optimize.unpack_method_calls(False)
cdef class StaticBody(object_body):
    def __cinit__(self, *args, **kwargs):
        pass

    def __init__(self, int id, CartesianPlane plane, int vertex_count):
        if plane.parent_vector is None:
            raise AttributeError("A body can't be made from a base plane, Use child plane instead!")
        super().__init__(id, STATIC, vertex_count)
        self.velocity = Vector2d(plane, 1, 0, 1, 1)
        self.velocity.rotate(pi/2)

    cpdef void USR_resolve_collision(self, object_body o, (double, double) dxy):
        if o.type == DYNAMIC:
            o.velocity.scale(self.friction_factor)
            o.shape.plane.parent_vector.set_head((o.shape.plane.parent_vector.head.x.num + dxy[0], o.shape.plane.parent_vector.head.y.num + dxy[1]))

@cython.optimize.unpack_method_calls(False)
cdef class DynamicBody(object_body):
    def __cinit__(self, *args, **kwargs):
        pass

    def __init__(self, int id, CartesianPlane plane, int vertex_count, double max_speed=1):
        if plane.parent_vector is None:
            raise AttributeError("A body can't be made from a base plane, Use child plane instead!")
        super().__init__(id, DYNAMIC, vertex_count)
        self.max_speed = max_speed
        self.velocity = Vector2d(plane, 1, 0, max_speed, 1)
        self.velocity.rotate(pi/2)

    cpdef void USR_resolve_collision(self, object_body o, (double, double) dxy):
        if o.type == DYNAMIC:
            self.velocity.scale(self.friction_factor)
            o.velocity.scale(self.friction_factor)
            self.shape.plane.parent_vector.set_head((self.shape.plane.parent_vector.head.x.num + -dxy[0]/2, self.shape.plane.parent_vector.head.y.num + -dxy[1]/2))
            o.shape.plane.parent_vector.set_head((o.shape.plane.parent_vector.head.x.num + dxy[0]/2, o.shape.plane.parent_vector.head.y.num + dxy[1]/2))
        elif o.type == STATIC:
            self.velocity.scale(self.friction_factor)
            self.shape.plane.parent_vector.set_head((self.shape.plane.parent_vector.head.x.num + -dxy[0], self.shape.plane.parent_vector.head.y.num + -dxy[1]))

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
        if not self.is_following_dir:
            self.shape.rotate(angle)
            self.velocity.rotate(angle)

    def show(self, color=(0, 0, 0), bint show_vertex=False):
        super().show(color, show_vertex)
        self.velocity.show(color)


cdef class Ray(FreeBody):

    def __cinit__(self, *args, **kwargs):
        pass

    def __init__(self, int id, CartesianPlane plane, double length):
        super().__init__(id, plane, 1)
        self.radius = length
        self.shape = Line(plane, length)

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.initializedcheck(False)
    cpdef void scale(self, double factor):
        (<Vector2d>self.vertices[0]).scale(factor)

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.initializedcheck(False)
    def show(self, color=(0, 0, 0), bint show_vertex=False):
        self.shape.plane.parent_vector.update()


@cython.optimize.unpack_method_calls(False)
cdef class DynamicPolygonBody(DynamicBody):
    def __cinit__(self, *args, **kwargs):
        pass

    def __init__(self, int id, CartesianPlane plane, tuple size, int max_speed=1):
        super().__init__(id, plane, size.__len__(), max_speed)
        self.radius = max(size)
        self.shape = Polygon(plane, size)

@cython.optimize.unpack_method_calls(False)
cdef class DynamicRectangleBody(DynamicBody):
    def __cinit__(self, *args, **kwargs):
        pass

    def __init__(self, int id, CartesianPlane plane, tuple size, int max_speed=1):
        super().__init__(id, plane, 4, max_speed)
        self.radius = max(size)
        self.shape = Rectangle(plane, size)

@cython.optimize.unpack_method_calls(False)
cdef class DynamicTriangleBody(DynamicBody):
    def __cinit__(self, *args, **kwargs):
        pass

    def __init__(self, int id, CartesianPlane plane, tuple size, int max_speed=1):
        super().__init__(id, plane, 3, max_speed)
        self.radius = max(size)
        self.shape = Triangle(plane, size)

cdef class StaticPolygonBody(StaticBody):
    def __cinit__(self, *args, **kwargs):
        pass

    def __init__(self, int id, CartesianPlane plane, tuple size):
        super().__init__(id, plane, size.__len__())
        self.radius = max(size)
        self.shape = Polygon(plane, size)

cdef class StaticRectangleBody(StaticBody):
    def __cinit__(self, *args, **kwargs):
        pass

    def __init__(self, int id, CartesianPlane plane, tuple size):
        super().__init__(id, plane, 4)
        self.radius = max(size)
        self.shape = Rectangle(plane, size)

cdef class StaticTriangleBody(StaticBody):
    def __cinit__(self, *args, **kwargs):
        pass

    def __init__(self, int id, CartesianPlane plane, tuple size):
        super().__init__(id, plane, 3)
        self.radius = max(size)
        self.shape = Triangle(plane, size)

cdef class FreePolygonBody(FreeBody):
    def __cinit__(self, *args, **kwargs):
        pass

    def __init__(self, int id, CartesianPlane plane, tuple size):
        super().__init__(id, plane, size.__len__())
        self.radius = max(size)
        self.shape = Polygon(plane, size)
