import math


class Plane:

    def __init__(self,
                 screen_size: tuple,
                 mode: str = 'center', space=10) -> None:
        """
        @params:
        screen_size - (x ,y)
        mode - ('centered', 'x_plus', 'x_negative', 'y_plus', 'y_negative'
                'I', 'II', 'III', 'IV') cartesian quadrants
        space - pixel count for 1 unit length in cartesian system
        """
        self.__x_dif, self.__y_dif = 0, 0
        self.__scree_size = screen_size
        self.__mode = mode
        self.space = 10
        if self.__mode == 'center':
            self.__x_dif = self.__scree_size[0] // 2
            self.__y_dif = self.__scree_size[1] // 2
        elif self.__mode == 'x+':
            self.__y_dif = self.__scree_size[1] // 2
        elif self.__mode == 'x-':
            self.__x_dif = self.__scree_size[0]
            self.__y_dif = self.__scree_size[1] // 2
        elif self.__mode == 'y+':
            self.__x_dif = self.__scree_size[0] // 2
            self.__y_dif = self.__scree_size[1]
        elif self.__mode == 'y-':
            self.__x_dif = self.__scree_size[0] // 2
        elif self.__mode == 'I':
            self.__y_dif = self.__scree_size[1]
        elif self.__mode == 'II':
            self.__x_dif = self.__scree_size[0]
            self.__y_dif = self.__scree_size[1]
        elif self.__mode == 'III':
            self.__x_dif = self.__scree_size[0]
        elif self.__mode == 'IV':
            ...
        else:
            raise ValueError('Unsupported mode!')

    @property
    def center(self):
        return (self.__x_dif, self.__y_dif)

    def getX(self, x):
        """Return real x coordinate in pygame coordinate system"""
        return self.__x_dif + x * self.space

    def getY(self, y):
        """Return real y coordinate in pygame coordinate system"""
        return self.__y_dif - y * self.space

    def toX(self, x):
        """Return real x coordinate in cartesian system"""
        return (x - self.__x_dif) / self.space

    def toY(self, y):
        """Return real y coordinate in cartesian system"""
        return (self.__y_dif - y) / self.space


class Vector:

    def __init__(self, x, y, plane: Plane) -> None:
        self.plane = plane
        self.x = x
        self.y = y

    @property
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    @property
    def direction(self):
        return math.atan2(self.y, self.x)

    @property
    def X(self):
        return self.plane.getX(self.x)

    @property
    def Y(self):
        return
