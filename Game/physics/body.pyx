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
            self.acceleration = Vector2d(space, 1, 0, 100, 1)
            self.velocity = Vector2d(space, 1, 0, 200, 1)
        else:
            self.acceleration = Vector2d(space, 0, 0, 0, 0)
            self.velocity = Vector2d(space, 0, 0, 0, 0)

    @cython.cdivision(True)
    cdef void react(self, Vector2d pos):
        cdef double a_len = floor(self.acceleration.length() * 100.0) / 100.0
        if a_len > 1:
            self.velocity.add_xy((self.acceleration._head._x._num / self.factor, self.acceleration._head._y._num / self.factor))
            self.acceleration.scale(0.81)
        else:
            self.acceleration.set_xy(self.acceleration.unit_vector(1))
        cdef double v_len = floor(self.velocity.length() * 100.0) / 100.0
        if v_len > 1:
            pos.add_xy((self.velocity._head._x._num / self.factor, self.velocity._head._y._num / self.factor))
            self.velocity.scale(0.99)
        else:
            self.velocity.set_xy(self.velocity.unit_vector(1))


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
        self.body.acceleration.rotate(pi/2)
        self.body.velocity.rotate(pi/2)

    cpdef void step(self):
        self.body.react(self.shape.plane.parent_vector)

    cpdef void accel(self, double factor):
        self.body.acceleration.add(factor)

    @cython.cdivision(True)
    cpdef void stop(self, double factor):
        self.body.velocity.scale(1/factor)

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.initializedcheck(False)
    cpdef void rotate(self, double angle):
        cdef int i
        for i in range(self.shape.vertex_count):
            (<Vector2d>self.shape.vertices[i]).rotate(angle)
        self.body.acceleration.rotate(angle)
        self.body.velocity.rotate(angle)

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
                heads.append(self.vertices[i].HEAD)
        else:
            for i in range(self.shape.vertex_count):
                heads.append(self.shape.vertices[i].HEAD)
        aalines(self.shape.window, color, True, heads)
        # self.body.velocity.show(window, (255, 0, 0))
        self.body.acceleration.show((0, 0, 255))


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
