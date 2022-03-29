class Plane:

    def __init__(self,
                 screen_size: tuple(int, int),
                 mode: str = 'centered') -> None:
        """
        screen_size (x ,y)
        mode ('centered', 'x_plus', 'x_negative', 'y_plus', 'y_negative'
              'I', 'II', 'III', 'IV') cartesian quadrants
        """
        self.__x_dif, self.__y_dif = 0
        self.__scree_size = screen_size
        self.__mode = mode
        if self.__mode == 'centered':
            self.__x_dif = self.__scree_size[0] // 2
            self.__y_dif = self.__scree_size[1] // 2
        elif self.__mode == 'x_plus':
            self.__y_dif = self.__scree_size[1] // 2
        elif self.__mode == 'x_negative':
            self.__x_dif = self.__scree_size[0]
            self.__y_dif = self.__scree_size[1] // 2
        elif self.__mode == 'y_plus':
            self.__x_dif = self.__scree_size[0] // 2
            self.__y_dif = self.__scree_size[1]
        elif self.__mode == 'y_negative':
            self.__x_dif = self.__scree_size[0] // 2
        elif self.__mode == 'I':
            self.__y_dif = self.__scree_size[1]
        elif self.__mode == 'II':
            self.__x_dif = self.__scree_size[0]
            self.__y_dif = self.__scree_size[1]
        elif self.__mode == 'III':
            ...





