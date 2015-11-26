#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses


class CursesMenu(object):
    """docstring for CursesMenu"""
    def __init__(self, items):
        self._screen = curses.initscr()
        self._items = items
        self.num_sel = 0
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        self._screen.keypad(1)

    def __del__(self):
        curses.endwin()


    def drawHeader(self, invoke=True):
        self._screen.erase()
        self._screen.border(0)
        """Initial values of vertical and horizontal indent"""
        y = 2
        x = 2
        """
        Lovely pep8 analyzer things that long lines is PURE EVIL!!!
        So I've had to declarate local variable for strings
        """
        s = "My lovely menu"
        self._screen.addstr(y, x, s, curses.A_STANDOUT)
        y += 2
        if invoke:
            s = "Please choose one of the next items"
            self._screen.addstr(y, x, s, curses.A_BOLD)
        """That was header. Main content will be put little to the right"""
        y += 1
        x += 2
        return y, x

    def draw(self):
        """Styles for sel and not sel menu items"""
        SEL = curses.color_pair(1)
        NOT_SEL = curses.A_NORMAL
        y, x = self.drawHeader()
        num = 0
        for i in self._items:
            style = SEL if num == self.num_sel else NOT_SEL
            self._screen.addstr(y, x, '{0}. {1}'.format(num, i), style)
            num += 1
            y += 1
        y += 1
        style = SEL if self.num_sel == len(self._items) else NOT_SEL
        self._screen.addstr(y, x, "0. Exit", style)
        self._screen.refresh()
        ch = self._screen.getch()
        return self.processInput(ch)

    def processInput(self, c):
        def increaseNum():
            if self.num_sel == len(self._items):
                return -1
            self.num_sel += 1
            return -1

        def decreaseNum():
            if self.num_sel == 0:
                return -1
            self.num_sel -= 1
            return -1

        def showItem():
            if self.num_sel == len(self._items):
                correctExit()
            y, x = self.drawHeader(False)
            s = '{}: {}'.format(self.num_sel, self._items[self.num_sel])
            self._screen.addstr(14, 15, "You chose: ", curses.A_NORMAL)
            self._screen.addstr(15, 15, s, curses.A_BOLD)
            self._screen.getch()
            return self.num_sel

        def correctExit():
            curses.endwin()
            exit()

        handlers = {
            ord('0'): correctExit,
            ord('q'): correctExit,
            ord('Q'): correctExit,
            ord('\n'): showItem,  # dunno why curses.KEY_ENTER doesn't work :(
            curses.KEY_UP: decreaseNum,
            curses.KEY_DOWN: increaseNum
        }
        if c not in handlers:
            self._screen.erase()
            cc = chr(c) if c < 256 else 'UNKNOWN'
            s = "Oops, input {0}('{1}') was not recognized! :(".format(c, cc)
            self._screen.addstr(15, 15, s, curses.A_BOLD)
            self._screen.getch()
            return -1
        else:
            return handlers[c]()
