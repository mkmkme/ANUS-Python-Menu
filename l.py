#!/usr/bin/env python3

from CursesMenu import CursesMenu

if __name__ == '__main__':
    m = CursesMenu('menu', ['one', 'two', 'three'])
    while True:
        m.draw()
