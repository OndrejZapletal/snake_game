#!/usr/bin/env python3

"""Implementation of Snake game that is using curses library to provide game UI."""
from random import randint
import curses
import sys
import time

WIDTH = 50
HEIGHT = 50
TIME_DELAY = 1
CELL_TYPE = ("  ", ("/\\", "\\/", "<=", "=>"), "##", "<>")


class Game(object):

    """Serving game mechanics."""

    def __init__(self, width, heigth):
        self.screen = curses.initscr()
        self.hei = width
        self.wid = heigth
        self._restrict_size()

        self.food = Food(self.wid, self.hei)
        self.snake = Snake(self.wid, self.hei, self.food)
        self.canvas = Canvas(self.wid, self.hei, self.snake, self.food)

        self.score = 0
        self.length = 1
        self.start_time = time.time()
        self.direction = (0, 1)

        self.screen.keypad(True)
        curses.halfdelay(TIME_DELAY)
        curses.noecho()

    def _restrict_size(self):
        maxheigth, maxwidth = self.screen.getmaxyx()
        if self.hei > maxheigth - 10:
            self.hei = maxheigth - 10

        if self.wid * 2 + 2 > maxwidth:
            self.wid = int((maxwidth / 2) - 2)

    def _update_game(self):
        self._step()
        self._draw_on_screen()

    def _step(self):
        self.snake.move(self.direction)
        if self._wrong_move():
            self._game_over()
        else:
            if self._food_found():
                self.snake.feed()
                self.canvas.create_food()
                self.score += 100
                self.length += 1

            self.canvas.update()

    def _food_found(self):
        return self.canvas.content[self.snake.y_pos][self.snake.x_pos] == 3

    def _wrong_move(self):
        result = False
        for tail_position in self.snake.tail:
            if tail_position == (self.snake.y_pos, self.snake.x_pos):
                result = True
        return result

    def _draw_on_screen(self):
        self.screen.erase()
        self.screen.addstr(0, 0, str(self.canvas))
        self.screen.addstr(self.hei + 3, 0, "Current Score: " + str(self.score))
        self.screen.addstr(self.hei + 4, 0, "Snake length: " + str(self.length))
        self.screen.addstr(self.hei + 5, 0, "Time: %.1f s" % (time.time() - self.start_time))
        self.screen.addstr(self.hei + 7, 0, "")

    def _game_over(self):
        self.screen.addstr(self.hei + 7, 0, "Game Over!", curses.A_BOLD)
        self.screen.addstr(self.hei + 9, 0, "Do you want to restart game? (y/n):")
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

    def _change_direction(self, direction):
        if not self.direction[0] == - direction[0] and not self.direction[1] == - direction[1]:
            self.direction = direction
            if direction == (1, 0):
                self.snake.direction = 0
            elif direction == (-1, 0):
                self.snake.direction = 1
            elif direction == (0, -1):
                self.snake.direction = 2
            elif direction == (0, 1):
                self.snake.direction = 3

    def play(self):
        """Starts gameplay"""
        key = ''
        while key != ord('q'):
            self._update_game()
            key = self.screen.getch()
            self.screen.refresh()
            if key == curses.KEY_UP:
                self._change_direction((1, 0))
            elif key == curses.KEY_DOWN:
                self._change_direction((-1, 0))
            elif key == curses.KEY_LEFT:
                self._change_direction((0, -1))
            elif key == curses.KEY_RIGHT:
                self._change_direction((0, 1))
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()


class Canvas(object):

    """This class will represent game canvas."""

    def __init__(self, width, height, snake, food):
        self.wid = width
        self.height = height
        self.food = food
        self.snake = snake
        self.content = []
        self._clear()
        self.update()

    def __repr__(self):
        representation = "|" + "-" * (((len(self.content[0])) * len(CELL_TYPE[0]))) + "|\n"
        for row in self.content:
            representation += "|"
            for cell in row:
                if cell == 1:
                    representation += CELL_TYPE[cell][self.snake.direction]
                else:
                    representation += CELL_TYPE[cell]
            representation += "|\n"
        representation += "|" + "-" * ((len(self.content[0])) * len(CELL_TYPE[0])) + "|\n"
        return representation

    def _clear(self):
        self.content = []
        for _ in range(self.height):
            self.content.append([0] * self.wid)

    def update(self):
        """Method updates food and snake position on canvas."""
        self._clear()
        for point in self.snake.tail:
            self.content[point[0]][point[1]] = 2
        self.content[self.snake.y_pos][self.snake.x_pos] = 1
        self.content[self.food.y_pos][self.food.x_pos] = 3

    def create_food(self):
        """Method creates food on random position on canvas."""
        invalid = True
        while invalid:
            x_pos = randint(3, self.wid - 3)
            y_pos = randint(3, self.height - 3)
            if self.content[y_pos][x_pos] == 0:
                invalid = False
                self.food.update_position(x_pos, y_pos)


class Snake(object):

    """Represent snake head and its tail"""

    def __init__(self, width, height, food):
        self.can_width = width
        self.can_height = height
        self.tail = []
        self.direction = 3
        invalid = True
        while invalid:
            self.x_pos = randint(3, width - 3)
            self.y_pos = randint(3, height - 3)
            if food.y_pos != self.y_pos and food.x_pos != self.x_pos:
                invalid = False

    def _restrict_position(self):
        if self.x_pos >= self.can_width:
            self.x_pos = 0
        elif self.x_pos < 0:
            self.x_pos = self.can_width - 1
        if self.y_pos >= self.can_height:
            self.y_pos = 0
        elif self.y_pos < 0:
            self.y_pos = self.can_height - 1

    def restart_snake(self, canvas_content):
        """Restart position and tale of snake."""
        self.tail = []
        invalid = True
        while invalid:
            self.x_pos = randint(3, self.can_width - 3)
            self.y_pos = randint(3, self.can_height - 3)
            if canvas_content[self.y_pos][self.x_pos] == 0:
                invalid = False

    def move(self, direction):
        """Moves snakes position and its tail."""
        for i in range(len(self.tail)-1):
            self.tail[i] = self.tail[i + 1]
        if len(self.tail) > 0:
            self.tail[len(self.tail) - 1] = (self.y_pos, self.x_pos)
        self.y_pos -= direction[0]
        self.x_pos += direction[1]
        self._restrict_position()

    def feed(self):
        """Expand snakes tail after feeding."""
        self.tail.insert(0, (self.y_pos, self.x_pos))


class Food(object):

    """Represents Food for snake."""

    def __init__(self, width, heigth):
        self.wid = width
        self.hei = heigth
        self.x_pos = randint(3, self.wid - 3)
        self.y_pos = randint(3, self.hei - 3)

    def update_position(self, x_pos, y_pos):
        """Update position of food."""
        self.x_pos = x_pos
        self.y_pos = y_pos


new_game = Game(WIDTH, HEIGHT)
new_game.play()
