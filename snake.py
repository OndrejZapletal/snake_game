from random import randint
import ipdb

WIDTH = 10
HEIGHT = 10
cell_type = (" ", "#", "*")


class Game(object):
    """Serving game mechanics."""

    def __init__(self, width, height):
        self.canvas = Canvas(width, height)
        self.snake = Snake(width, height)
        self.canvas.set_snake(self.snake)
        self.canvas.set_food()

    def move(self, x, y):
        self.snake.move(x, y)
        self.canvas.set_snake(self.snake)

    def show(self):
        print(self.canvas)


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

    def move(self, x, y):
        self.x += x
        self.y -= y
        if self.x >= self.can_width:
            self.x = self.can_width - 1
        elif self.x < 0:
            self.x = 0

        if self.y >= self.can_height:
            self.y = self.can_height - 1
        elif self.y < 0:
            self.y = 0

new_game = Game(WIDTH, HEIGHT)
new_game.move(0, 1)
new_game.show()
new_game.move(0, 1)
new_game.show()
new_game.move(1, 0)
new_game.show()
new_game.move(1, 0)
new_game.show()
