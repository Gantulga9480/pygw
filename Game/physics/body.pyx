import cython
from Game.graphic.cartesian cimport CartesianPlane, Vector2d
from Game.graphic.shapes cimport polygon
from Game.math.core cimport pi
from pygame.draw import aalines


STATIC = 0
DYNAMIC = 1


cdef class body_dynamics:

    def __cinit__(self, *args, **kwargs):
        ...

    def __init__(self, CartesianPlane space, int body_type) -> None:
        if body_type == DYNAMIC:
            self.acceleration = Vector2d(space, 1, 0, 10)
            self.velocity = Vector2d(space, 1, 0, 200)
        else:
            self.acceleration = Vector2d(space, 0, 0, 0)
            self.velocity = Vector2d(space, 0, 0, 0)

    @cython.cdivision(True)
    cdef void react(self, Vector2d pos, double factor):
        cdef int a_len = <int>(self.acceleration.length() * 100.0 % 100)
        if a_len > 0:
            self.velocity.add_xy(self.acceleration.get_xy())
            self.acceleration.scale(1/1.1)
        else:
            self.acceleration.set_xy(self.acceleration.unit_vector(1))
        cdef int v_len = <int>(self.velocity.length() * 100 % 100)
        if v_len > 0:
            pos.add_xy((self.velocity._head._x._num / factor, self.velocity._head._y._num / factor))
            self.velocity.add(v_len * -0.01)
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
                 bint limit_vertex=1,
                 int speed_factor=60) -> None:
        plane = CartesianPlane((size, size), 1, pos)
        super().__init__(plane, vertex_count, size, limit_vertex)
        self.id = body_id
        self.type = body_type
        self.radius = size
        self.speed_factor = speed_factor
        self.body = body_dynamics(plane, body_type)
        self.body.acceleration.rotate(pi/2)
        self.body.velocity.rotate(pi/2)

    cpdef void step(self):
        self.body.react(self.plane.parent_vector, self.speed_factor)

    @cython.cdivision(True)
    cpdef void accel(self, double factor):
        self.body.acceleration.add(factor)

    @cython.cdivision(True)
    cpdef void stop(self, double factor):
        self.body.acceleration.scale(factor)

    @cython.cdivision(True)
    cpdef void rotate(self, double angle):
        cdef int i
        cdef double a = angle / self.speed_factor
        for i in range(self.vertex_count):
            (<Vector2d>self.vertices[i]).rotate(a)
        self.body.acceleration.rotate(a)
        self.body.velocity.rotate(a)

    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.nonecheck(False)
    def show(self, window, color, width, show_vertex):
        cdef int i
        cdef list heads = []
            # self.position_vec.show(window)
        for i in range(self.vertex_count):
            if show_vertex:
                (<Vector2d>self.vertices[i]).show(window, color, width)
            heads.append(self.vertices[i].HEAD)
        # if aa:
        aalines(window, color, True, heads, width)
        # self.body.velocity.show(window, color, 1)
        self.body.acceleration.show(window, (0, 0, 255), 3)
        # else:
        #     pg.draw.lines(window, color, True,
        #                   [vertex.HEAD for vertex in self.vertices], width)

