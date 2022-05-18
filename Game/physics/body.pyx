import cython
from Game.graphic.cartesian cimport CartesianPlane, Vector2d
from Game.graphic.shapes cimport polygon
from Game.math.core cimport pi
from pygame.draw import aalines
from libc.math cimport floor


STATIC = 0
DYNAMIC = 1


cdef class body_dynamics:

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self, CartesianPlane space, int body_type) -> None:
        self.factor = 60
        if body_type == DYNAMIC:
            self.acceleration = Vector2d(space, 1, 0, 10)
            self.velocity = Vector2d(space, 1, 0, 200)
        else:
            self.acceleration = Vector2d(space, 0, 0, 0)
            self.velocity = Vector2d(space, 0, 0, 0)

    @cython.cdivision(True)
    cdef void react(self, Vector2d pos):
        cdef double a_len = floor(self.acceleration.length() * 100.0) / 100.0
        if a_len > 1:
            self.velocity.add_xy(self.acceleration.get_xy())
            self.acceleration.scale(0.81)
        else:
            self.acceleration.set_xy(self.acceleration.unit_vector(1))
        cdef double v_len = floor(self.velocity.length() * 100.0) / 100.0
        if v_len > 1:
            pos.add_xy((self.velocity._head._x._num / self.factor, self.velocity._head._y._num / self.factor))
            self.velocity.scale(0.99)
        else:
            self.velocity.set_xy(self.velocity.unit_vector(1))


cdef class base_body(polygon):

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self,
                 int body_id,
                 int body_type,
                 Vector2d pos,
                 int vertex_count=2,
                 double size=1,
                 bint limit_vertex=1) -> None:
        plane = CartesianPlane((size, size), 1, pos)
        super().__init__(plane, vertex_count, size, limit_vertex)
        self.id = body_id
        self.type = body_type
        self.radius = size
        self.body = body_dynamics(plane, body_type)
        self.body.acceleration.rotate(pi/2)
        self.body.velocity.rotate(pi/2)

    cpdef void step(self):
        self.body.react(self.plane.parent_vector)

    @cython.cdivision(True)
    cpdef void accel(self, double factor):
        self.body.acceleration.add(factor)

    @cython.cdivision(True)
    cpdef void stop(self, double factor):
        self.body.velocity.scale(1/factor)

    @cython.cdivision(True)
    cpdef void rotate(self, double angle):
        cdef int i
        for i in range(self.vertex_count):
            (<Vector2d>self.vertices[i]).rotate(angle)
        self.body.acceleration.rotate(angle)
        self.body.velocity.rotate(angle)

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.nonecheck(False)
    def show(self, window, color, show_vertex=False):
        cdef int i
        cdef list heads = []
        if show_vertex:
            # self.position_vec.show(window)
            for i in range(self.vertex_count):
                (<Vector2d>self.vertices[i]).show(window, color)
                heads.append(self.vertices[i].HEAD)
        else:
            for i in range(self.vertex_count):
                heads.append(self.vertices[i].HEAD)
        aalines(window, color, True, heads)
        # self.body.velocity.show(window, (255, 0, 0))
        self.body.acceleration.show(window, (0, 0, 255))
