import cython
from Game.graphic.cartesian cimport CartesianPlane, Vector2d
from Game.graphic.shapes cimport Polygon, Rectangle, Triangle
from Game.math.core cimport pi
from pygame.draw import aalines
from libc.math cimport floor


STATIC = 0
DYNAMIC = 1


cdef class object_dynamics:

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self, CartesianPlane space, int body_type) -> None:
        self.factor = 60
        if body_type == DYNAMIC:
            self.a = Vector2d(space, 1, 0, 2, 1)
            self.v = Vector2d(space, 1, 0, 3, 1)
            self.a.rotate(pi/2)
            self.v.rotate(pi/2)
        else:
            self.a = Vector2d(space, 0, 0, 0, 0)
            self.v = Vector2d(space, 0, 0, 0, 0)

    @cython.cdivision(True)
    cdef void react(self, Vector2d pos):
        cdef double a_len = floor(self.a.mag() * 100.0) / 100.0
        if a_len > 1:
            self.v.add_xy(self.a.get_xy())
            self.a.scale(0.81)
        else:
            self.a.set_xy(self.a.unit_vector(1))
        cdef double v_len = floor(self.v.mag() * 100.0) / 100.0
        if v_len > 1:
            pos.add_xy(self.v.get_xy())
            self.v.scale(0.9)
        else:
            self.v.set_xy(self.v.unit_vector(1))


cdef class object_body:

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self,
                 int body_id,
                 int body_type,
                 CartesianPlane plane):
        self.id = body_id
        self.type = body_type
        self.body = object_dynamics(plane, body_type)

    cpdef void step(self):
        self.body.react(self.shape.plane.parent_vector)

    cpdef void accelerate(self, double factor):
        self.body.a.add(factor)

    @cython.cdivision(True)
    cpdef void stop(self, double factor):
        self.body.v.scale(1/factor)

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.initializedcheck(False)
    cpdef void rotate(self, double angle):
        cdef int i
        for i in range(self.shape.vertex_count):
            (<Vector2d>self.shape.vertices[i]).rotate(angle)
        self.body.a.rotate(angle)
        self.body.v.rotate(angle)

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.initializedcheck(False)
    def show(self, color, show_vertex=False):
        cdef int i
        cdef list heads = []
        if show_vertex:
            # self.position_vec.show(window)
            for i in range(self.shape.vertex_count):
                (<Vector2d>self.shape.vertices[i]).show(color)
                heads.append((<Vector2d>self.shape.vertices[i]).get_HEAD())
        else:
            for i in range(self.shape.vertex_count):
                heads.append((<Vector2d>self.shape.vertices[i]).get_HEAD())
        aalines(self.shape.window, color, True, heads)
        self.body.v.show((255, 0, 0))
        self.body.a.show((0, 0, 255))


cdef class PolygonBody(object_body):

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self,
                 int body_id,
                 int body_type,
                 CartesianPlane plane,
                 tuple size):
        super().__init__(body_id, body_type, plane)
        self.radius = max(size)
        self.shape = Polygon(plane, size)


cdef class RectBody(object_body):

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self,
                 int body_id,
                 int body_type,
                 CartesianPlane plane,
                 tuple size):
        super().__init__(body_id, body_type, plane)
        self.radius = max(size)
        self.shape = Rectangle(plane, size)


cdef class TriangleBody(object_body):

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self,
                 int body_id,
                 int body_type,
                 CartesianPlane plane,
                 tuple size):
        super().__init__(body_id, body_type, plane)
        self.radius = max(size)
        self.shape = Triangle(plane, size)
