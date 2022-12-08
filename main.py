from Game import Game
from Game import core
import numpy as np

LEFT = 1
RIGHT = 0


class Main(Game):

    GRID_SIZE = 20
    W = GRID_SIZE * 40
    SPEED = 3
    PLATE_LEN = 5

    def __init__(self) -> None:
        super().__init__()

        self.size = (self.W, self.W)
        self.board = np.zeros((self.GRID_SIZE, self.GRID_SIZE))
        self.plate = np.zeros((self.PLATE_LEN, 2), dtype=int)
        self.ball = np.zeros((2), dtype=int)
        self.ball_hit_plate = False
        self.ball_dir = np.zeros((2), dtype=int)
        self.plate_dir = RIGHT

        self.counter = 0

    def move(self):
        # move plate
        if self.counter % self.SPEED == 0:
            if self.plate_dir == RIGHT:
                if self.plate[self.PLATE_LEN-1][1] < self.GRID_SIZE - 1:
                    for i in range(self.PLATE_LEN):
                        self.plate[i][1] += 1
            elif self.plate_dir == LEFT:
                if self.plate[0][1] > 0:
                    for i in range(self.PLATE_LEN):
                        self.plate[i][1] -= 1
        # move ball
        if self.counter % self.SPEED == 0:
            # wall check
            if self.ball[1] == 0 or self.ball[1] == self.GRID_SIZE - 1:
                self.ball_dir[1] *= -1
            # top check
            if self.ball[0] == 0:
                self.ball_dir = [1, 0]
            # plate check
            if self.ball[0] == self.GRID_SIZE - 2:
                ball_dir = self.check_ball()
                if ball_dir:
                    print('ball hit')
                    if ball_dir == 1:
                        self.ball_dir = [-1, -1]
                    elif 2 <= ball_dir <= 4:
                        self.ball_dir = [-1, 0]
                    elif ball_dir == 5:
                        self.ball_dir = [-1, 1]
                else:
                    print(self.ball)
                    self.setup()
                    print('Game over')
            self.ball[0] += self.ball_dir[0]
            self.ball[1] += self.ball_dir[1]
        self.counter += 1

    def check_ball(self):
        for i in range(self.PLATE_LEN):
            if self.plate[i][1] == self.ball[1]:
                return i+1
        return 0

    def place(self):
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                self.board[i][j] = 0

        for i in range(self.PLATE_LEN):
            self.board[self.plate[i][0]][self.plate[i][1]] = 1

        self.board[self.ball[0]][self.ball[1]] = 1

    def onEvent(self, event) -> None:
        if event.type == core.KEYUP:
            if event.key == core.K_LEFT:
                self.plate_dir = LEFT
            elif event.key == core.K_RIGHT:
                self.plate_dir = RIGHT

    def setup(self) -> None:
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                self.board[i][j] = 0

        for i in range(self.PLATE_LEN):
            self.plate[i][0] = self.GRID_SIZE - 1
            self.plate[i][1] = i + 3

        self.ball[0] = 3
        self.ball[1] = 3
        self.ball_dir[0] = 1
        self.ball_dir[1] = 0
        self.ball_hit_plate = False

    def loop(self):
        self.place()
        self.move()

    def onRender(self) -> None:
        self.window.fill((0, 0, 0))
        self.draw_grid()
        self.disp()

    def draw_grid(self):
        w = int(self.W / self.GRID_SIZE)
        for i in range(self.GRID_SIZE+1):
            core.draw.line(self.window, (100, 100, 100), (w*i, 1), (w*i, self.W-1))
            core.draw.line(self.window, (100, 100, 100), (1, w*i), (self.W-1, w*i))

    def disp(self):
        w = int(self.W / self.GRID_SIZE)
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                if self.board[i][j] == 1:
                    core.draw.rect(self.window, (200, 0, 0), (w*j+1, w*i+1, w-1, w-1))


Main().loop_forever()
