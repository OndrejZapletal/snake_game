#!/usr/bin/env python3

"""Implementation of Snake game that is using curses library to provide game UI."""
from random import randint
import curses
import sys
import time

WIDTH = 50
HEIGHT = 50
TIME_DELAY = 1
CELL_TYPE = ("  ", "<>", "##")
HEAD = ("/\\", "\\/", "<=", "=>")
DIRECTION = ((1, 0), (-1, 0), (0, -1), (0, 1))


class Game(object):

    """Serving game mechanics."""

    def __init__(self, width, heigth):
        self.screen = curses.initscr()
        self.heigth = width
        self.width = heigth
        self._restrict_size()

        self.food = Food(self.width, self.heigth)
        self.snake = Snake(self.width, self.heigth, self.food)
        self.canvas = Canvas(self.width, self.heigth, self.food, self.snake)

        self.score = 0
        self.length = 1
        self.start_time = time.time()

        self.screen.keypad(True)
        curses.halfdelay(TIME_DELAY)
        curses.noecho()

    def _restrict_size(self):
        maxheigth, maxwidth = self.screen.getmaxyx()
        if self.heigth > maxheigth - 10:
            self.heigth = maxheigth - 10

        if self.width * 2 + 2 > maxwidth:
            self.width = int((maxwidth / 2) - 2)

    def _update_game(self):
        self._step()
        self._draw_canvas()
        self._draw_snake()

    def _step(self):
        self.snake.move()
        if self._wrong_move():
            self._game_over()
        else:
            if self._food_found():
                self.snake.feed()
                self.canvas.create_food()
                self.score += 100
                self.length += 1
                self.screen.addstr(self.heigth + 7, 0, "Food Fond")

            self.canvas.update()

    def _food_found(self):
        return not self.food.empty(self.snake.y_pos, self.snake.x_pos)

    def _wrong_move(self):
        result = False
        for tail_position in self.snake.tail:
            if tail_position == (self.snake.y_pos, self.snake.x_pos):
                result = True
        return result

    def _draw_canvas(self):
        self.screen.erase()
        self.screen.addstr(0, 0, str(self.canvas))
        self.screen.addstr(self.heigth + 3, 0, "Current Score: " + str(self.score))
        self.screen.addstr(self.heigth + 4, 0, "Snake length: " + str(self.length))
        self.screen.addstr(self.heigth + 5, 0, "Time: %.1f s" % (time.time() - self.start_time))
        self.screen.addstr(self.heigth + 7, 0, "")

    def _draw_snake(self):
        for position in self.snake.tail:
            self.screen.addstr(position[0] + 1, position[1] * 2 + 1, CELL_TYPE[2])
        self.screen.addstr(
            self.snake.y_pos + 1, self.snake.x_pos * 2 + 1, HEAD[self.snake.direction])
        self.screen.addstr(self.heigth + 7, 0, "")

    def _game_over(self):
        self.screen.addstr(self.heigth + 7, 0, "Game Over!", curses.A_BOLD)
        self.screen.addstr(self.heigth + 9, 0, "Do you want to restart game? (y/n):")
        while True:
            key = self.screen.getch()
            if key == ord('y'):
                self.screen.erase()
                self.canvas.create_food()
                self.snake.restart_snake(self.canvas.content)
                self.length = 1
                break
            elif key == ord('n'):
                curses.nocbreak()
                self.screen.keypad(False)
                curses.echo()
                curses.endwin()
                sys.exit()

    def play(self):
        """Starts gameplay"""
        key = ''
        while key != ord('q'):
            self._update_game()
            key = self.screen.getch()
            self.screen.refresh()
            if key == curses.KEY_UP or \
               key == ord('k') or \
               key == ord('w'):
                self.snake.change_direction(0)
            elif key == curses.KEY_DOWN or \
                 key == ord('j') or \
                 key == ord('s'):
                self.snake.change_direction(1)
            elif key == curses.KEY_LEFT or \
                 key == ord('h') or \
                 key == ord('a'):
                self.snake.change_direction(2)
            elif key == curses.KEY_RIGHT or \
                 key == ord('l') or \
                 key == ord('d'):
                self.snake.change_direction(3)
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()


class Canvas(object):

    """This class will represent game canvas."""

    def __init__(self, width, height, food, snake):
        self.width = width
        self.height = height

        self.food = food
        self.snake = snake
        self.content = []

        self._clear()
        self.update()

    def __repr__(self):
        representation = "|" + "-" * self.width * len(CELL_TYPE[0]) + "|\n"
        for row in self.content:
            representation += "|"
            for cell in row:
                representation += CELL_TYPE[cell]
            representation += "|\n"
        representation += "|" + "-" * self.width * len(CELL_TYPE[0]) + "|\n"
        return representation

    def _clear(self):
        self.content = []
        for _ in range(self.height):
            self.content.append([0] * self.width)

    def update(self):
        """Method updates food and snake position on canvas."""
        self._clear()
        self.content[self.food.y_pos][self.food.x_pos] = 1

    def create_food(self):
        """Method creates food on random position on canvas."""
        while True:
            x_pos = randint(3, self.width - 3)
            y_pos = randint(3, self.height - 3)
            if self.snake.empty(y_pos, x_pos):
                self.food.update_position(x_pos, y_pos)
                break


class Snake(object):

    """Represent snake head and its tail"""

    def __init__(self, width, height, food):
        self.can_width = width
        self.can_height = height
        self.tail = []
        self.direction = 3
        while True:
            self.x_pos = randint(3, width - 3)
            self.y_pos = randint(3, height - 3)
            if food.y_pos != self.y_pos and food.x_pos != self.x_pos:
                break

    def _restrict_position(self):
        if self.x_pos >= self.can_width:
            self.x_pos = 0
        elif self.x_pos < 0:
            self.x_pos = self.can_width - 1
        if self.y_pos >= self.can_height:
            self.y_pos = 0
        elif self.y_pos < 0:
            self.y_pos = self.can_height - 1

    def change_direction(self, index):
        if not DIRECTION[self.direction][0] == - DIRECTION[index][0] and \
           not DIRECTION[self.direction][1] == - DIRECTION[index][1]:
            self.direction = index

    def empty(self, y, x):
        empty = True
        for position in self.tail:
            if position[0] == y and position[1] == x:
                empty = False
        if self.y_pos == y and self.x_pos == x:
            empty = False
        return empty

    def restart_snake(self, canvas_content):
        """Restart position and tale of snake."""
        self.tail = []
        while True:
            self.x_pos = randint(3, self.can_width - 3)
            self.y_pos = randint(3, self.can_height - 3)
            if canvas_content[self.y_pos][self.x_pos] == 0:
                break

    def move(self):
        """Moves snakes position and its tail."""
        for i in reversed(range(1, len(self.tail))):
            self.tail[i] = self.tail[i - 1]

        if len(self.tail) > 0:
            self.tail[0] = (self.y_pos, self.x_pos)

        self.y_pos -= DIRECTION[self.direction][0]
        self.x_pos += DIRECTION[self.direction][1]

        self._restrict_position()

    def feed(self):
        """Expand snakes tail after feeding."""
        self.tail.append((self.y_pos, self.x_pos))


class Food(object):

    """Represents Food for snake."""

    def __init__(self, width, heigth):
        self.width = width
        self.heigth = heigth
        self.x_pos = randint(3, self.width - 3)
        self.y_pos = randint(3, self.heigth - 3)

    def update_position(self, x_pos, y_pos):
        """Update position of food."""
        self.x_pos = x_pos
        self.y_pos = y_pos

    def empty(self, y, x):
        return not self.x_pos == x or not self.y_pos == y


new_game = Game(WIDTH, HEIGHT)
new_game.play()
