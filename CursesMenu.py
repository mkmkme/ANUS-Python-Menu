#!/usr/bin/env python

import curses


class CursesMenu(object):
    """docstring for CursesMenu"""
    def __init__(self, screen, items):
        self._screen = screen
        self._items = items
        self.num_selected = 0
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        self._screen.keypad(1)

    def draw(self):
        """Styles for selected and not selected menu items"""
        SELECTED = curses.color_pair(1)
        NOT_SELECTED = curses.A_NORMAL
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
        s = "Please choose one of the next items"
        self._screen.addstr(y, x, s, curses.A_BOLD)
        """That was header. Main content will be put little to the right"""
        y += 1
        x += 2
        num = 0
        for i in self._items:
            style = SELECTED if num == self.num_selected else NOT_SELECTED
            self._screen.addstr(y, x, '{0}. {1}'.format(num, i), style)
            num += 1
            y += 1
        self._screen.refresh()
        ch = self._screen.getch()
        self.processInput(ch)

    def processInput(self, c):
        def increaseNum():
            self.num_selected += 1

        def decreaseNum():
            self.num_selected -= 1

        def correctExit():
            curses.endwin()
            exit()

        handlers = {
            ord('0'): correctExit,
            curses.KEY_UP: decreaseNum,
            curses.KEY_DOWN: increaseNum
        }
        if c not in handlers:
            self._screen.erase()
            s = "Oops, input '{0}' was not recognized! :(".format(chr(c))
            self._screen.addstr(15, 15, s, curses.A_BOLD)
            self._screen.getch()
        else:
            handlers[c]()
            self.draw()


def main():
    scr = curses.initscr()
    items = [
        "Ivan Ivanoff",
        "Petr Petroff",
        "Sidor Sidoroff",
        "Ushat Pomoev",
        "Rulon Oboev"
    ]
    menu = CursesMenu(scr, items)
    while True:
        menu.draw()

if __name__ == "__main__":
    main()
