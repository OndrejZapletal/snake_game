from random import randint
import curses
import ipdb

WIDTH = 50
HEIGHT = 50
TIME_DELAY = 2
cell_type = ("  ", "##", "**")


class Game(object):
    """Serving game mechanics."""

    def __init__(self, width, height):
        self.canvas = Canvas(width, height)
        self.snake = Snake(width, height)
        self.canvas.set_snake(self.snake)
        self.canvas.set_food()
        self.direction = (0, 1)
        self.screen = curses.initscr()
        curses.halfdelay(TIME_DELAY)
        self.screen.keypad(1)

    def update_game(self):
        self.move()
        self.show(self.screen)

    def play(self):
        key = ''
        while key != ord('q'):
            self.update_game()
            key = self.screen.getch()
            self.screen.refresh()
            if key == curses.KEY_UP:
                self.up()
            elif key == curses.KEY_DOWN:
                self.down()
            elif key == curses.KEY_LEFT:
                self.left()
            elif key == curses.KEY_RIGHT:
                self.right()
        curses.endwin()

    def move(self):
        self.snake.move(self.direction)

        self.canvas.set_snake(self.snake)

    def show(self, screen):
        screen.erase()
        screen.addstr(0,0, str(self.canvas))

    def up(self):
        self.direction = (1, 0)

    def down(self):
        self.direction = (-1, 0)

    def left(self):
        self.direction = (0, -1)

    def right(self):
        self.direction = (0, 1)


class Canvas(object):

    """This class will represent game canvas."""

    def __init__(self, width, height):
        self.content = []
        for _ in range(height):
            self.content.append([0] * width)
        self.width = width
        self.height = height
        self.snake_x_pos = 0
        self.snake_y_pos = 0

    def __repr__(self):
        representation = "|" + "-" * ((len(self.content[0])) * len(cell_type[0])) + "|\n"
        for row in self.content:
            representation += "|"
            for cell in row:
                representation += cell_type[cell]
            representation += "|\n"
        representation += "|" + "-" * ((len(self.content[0])) * len(cell_type[0])) + "|\n"

        return representation

    def set_snake(self, snake):
        self.content[self.snake_y_pos][self.snake_x_pos] = 0
        self.content[snake.y][snake.x] = 1
        self.snake_x_pos = snake.x
        self.snake_y_pos = snake.y


    def set_food(self):
        invalid = True
        while invalid:
            x = randint(3, self.width - 3)
            y = randint(3, self.height - 3)
            if self.content[y][x] == 0:
                self.content[y][x] = 2
                invalid = False


class Snake(object):

    """Represent snake head and its tail"""

    def __init__(self, width, height):
        self.can_width = width
        self.can_height = height

        self.x = randint(3, width - 3)
        self.y = randint(3, height - 3)

    def move(self, direction):
        self.y -= direction[0]
        self.x += direction[1]
        if self.x >= self.can_width:
            self.x = self.can_width - 1
        elif self.x < 0:
            self.x = 0

        if self.y >= self.can_height:
            self.y = self.can_height - 1
        elif self.y < 0:
            self.y = 0




new_game = Game(WIDTH, HEIGHT)
new_game.play()
