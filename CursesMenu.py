# -*- coding: utf-8 -*-

import curses
import sys


class CursesMenu(object):
    """docstring for CursesMenu"""
    def __init__(self, screen, headerstr, items=[]):
        self._screen = screen
        self._headerstr = headerstr
        self._items = items
        self.num_sel = 0
        curses.start_color()
        curses.noecho()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        self._screen.keypad(1)

    def add(self, text, cb):
        self._items.append({'text': text, 'func': cb})

    def drawHeader(self, invoke=True):
        self._screen.erase()
        self._screen.border(0)
        # Initial values of vertical and horizontal indent
        y = 2
        x = 2
        s = self._headerstr
        self._screen.addstr(y, x, s, curses.A_STANDOUT)
        y += 2
        if invoke:
            self._screen.addstr(y, x, s, curses.A_BOLD)
        # That was header. Main content will be put little to the right
        x += 2
        y += 1
        return x, y

    def draw(self):
        # Styles for sel and not sel menu items
        SEL = curses.color_pair(1)
        NOT_SEL = curses.A_NORMAL
        x, y = self.drawHeader()
        num = 0
        for i in self._items:
            style = SEL if num == self.num_sel else NOT_SEL
            self._screen.addstr(y, x, '{0}. {1}'.format(num, i['text']), style)
            num += 1
            y += 1
        y += 1
        style = SEL if self.num_sel == len(self._items) else NOT_SEL
        self._screen.addstr(y, x, "0. Exit", style)
        self._screen.refresh()
        ch = self._screen.getch()
        return self.processInput(ch)

    def up(self):
        if self.num_sel == 0:
            return 0
        self.num_sel -= 1
        return 0

    def down(self):
        if self.num_sel == len(self._items):
            return 0
        self.num_sel += 1
        return 0

    def run(self):
        c = 0
        while c >= 0:
            c = self.draw()

    def print(self, s):
        self.drawHeader(False)
        self._screen.addstr(15, 15, s, curses.A_NORMAL)
        return 0

    def process_handlers(self):
        if self.num_sel == len(self._items):
            return -1
        return self._items[self.num_sel]['func']()

    def processInput(self, c):
        stop = lambda : -1
        handlers = {
            ord('0'): stop,
            ord('q'): stop,
            ord('Q'): stop,
            ord('\n'): self.process_handlers,
            curses.KEY_UP: self.up,
            curses.KEY_DOWN: self.down
        }
        if c not in handlers:
            self._screen.erase()
            cc = chr(c) if c < 256 else 'unprintable'
            s = "input {0}('{1}') was not recognized".format(c, cc)
            self._screen.addstr(15, 15, s, curses.A_BOLD)
            self._screen.getch()
            return 0
        else:
            return handlers[c]()
