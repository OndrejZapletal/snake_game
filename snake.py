"""Implementation of Snake game that is using curses library to provide game UI."""
from random import randint
import curses

WIDTH = 50
HEIGHT = 30
TIME_DELAY = 1
CELL_TYPE = ("  ", "##", "**")


class Game(object):
    """Serving game mechanics."""

    def __init__(self, width, heigth):
        self.food = Food(width, heigth)
        self.snake = Snake(width, heigth, self.food)
        self.canvas = Canvas(width, heigth, self.snake, self.food)

        self.direction = (0, 1)
        self.screen = curses.initscr()
        self.screen.keypad(1)
        curses.halfdelay(TIME_DELAY)

    def _update_game(self):
        self._move()
        self._show()

    def _move(self):
        self.snake.move(self.direction)

        if self.canvas.content[self.snake.y][self.snake.x] == 2:
            self.snake.feed()
            self.canvas.create_food()

        # self.food.refresh(self.canvas.content)
        self.canvas.update()

    def _show(self):
        self.screen.erase()
        self.screen.addstr(0, 0, str(self.canvas))

    def _up(self):
        self.direction = (1, 0)

    def _down(self):
        self.direction = (-1, 0)

    def _left(self):
        self.direction = (0, -1)

    def _right(self):
        self.direction = (0, 1)

    def play(self):
        key = ''
        while key != ord('q'):
            self._update_game()
            key = self.screen.getch()
            self.screen.refresh()
            if key == curses.KEY_UP:
                self._up()
            elif key == curses.KEY_DOWN:
                self._down()
            elif key == curses.KEY_LEFT:
                self._left()
            elif key == curses.KEY_RIGHT:
                self._right()
        curses.endwin()


class Canvas(object):

    """This class will represent game canvas."""

    def __init__(self, width, height, snake, food):
        self.width = width
        self.height = height
        self.food = food
        self.snake = snake

        self.content = []

        self._clear()
        self.update()

    def __repr__(self):
        representation = "|" + "-" * ((len(self.content[0])) * len(CELL_TYPE[0])) + "|\n"
        for row in self.content:
            representation += "|"
            for cell in row:
                representation += CELL_TYPE[cell]
            representation += "|\n"
        representation += "|" + "-" * ((len(self.content[0])) * len(CELL_TYPE[0])) + "|\n"
        return representation

    def _clear(self):
        self.content = []
        for _ in range(self.height):
            self.content.append([0] * self.width)

    def update(self):
        self._clear()
        for point in self.snake.tail:
            self.content[point[0]][point[1]] = 1
        self.content[self.snake.y][self.snake.x] = 1
        self.content[self.food.y][self.food.x] = 2

    def create_food(self):
        invalid = True
        while invalid:
            x = randint(3, self.width - 3)
            y = randint(3, self.height - 3)
            if self.content[y][x] == 0:
                invalid = False
                self.food.update_position(x, y)


class Snake(object):

    """Represent snake head and its tail"""

    def __init__(self, width, height, food):
        self.can_width = width
        self.can_height = height
        self.tail = []

        invalid = True
        while invalid:
            self.x = randint(3, width - 3)
            self.y = randint(3, height - 3)
            if food.y != self.y and food.x != self.x:
                invalid = False

    def _restrict_position(self):
        if self.x >= self.can_width:
            self.x = 0
        elif self.x < 0:
            self.x = self.can_width - 1

        if self.y >= self.can_height:
            self.y = 0
        elif self.y < 0:
            self.y = self.can_height - 1

    def move(self, direction):
        for i in range(len(self.tail)-1):
            self.tail[i] = self.tail[i + 1]
        if len(self.tail) > 0:
            self.tail[len(self.tail) - 1] = (self.y, self.x)

        self.y -= direction[0]
        self.x += direction[1]

        self._restrict_position()


    def feed(self):
        self.tail.insert(0, (self.y, self.x))


class Food(object):

    def __init__(self, width, heigth):
        self.width = width
        self.heigth = heigth
        self.x = randint(3, self.width - 3)
        self.y = randint(3, self.heigth - 3)

    def update_position(self, x, y):
        self.x = x
        self.y = y


new_game = Game(WIDTH, HEIGHT)
new_game.play()
