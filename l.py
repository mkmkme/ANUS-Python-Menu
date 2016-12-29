#!/usr/bin/env python3

import curses
from CursesMenu import CursesMenu

def foo():
    print('baaaang!')
    return 0

if __name__ == '__main__':
    s = curses.initscr()
    m = CursesMenu(s, 'menu')
    m.add('one', foo)
    m.add('two', foo)
    m.add('three', foo)
    try:
        m.run()
    except Exception:
        curses.endwin()
        raise
    else:
        curses.endwin()
