#!/usr/bin/python3
import curses
import time
import threading


def __init_color__():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)


def chunks(l, n):
    return list(zip(*[iter(l)]*n))


def bitblt(stdscr, screen, width, intrue, outtrue, outfalse):
    screen = chunks(screen, width)
    for j, k in zip(screen, range(len(screen))):
        for l, m in zip(j, range(len(j))):
            m = m*2
            stdscr.addstr(k, m, "  ", curses.color_pair(outtrue if l == intrue else outfalse))
    stdscr.refresh()


def __switcher__(stdscr):
    global __command__
    global _screens_
    global __execute__
    while __execute__:
        if isinstance(__command__, list):
            if isinstance(__command__[1], list):
                bitblt(__command__[0], __command__[1], _screens_["size"]["width"], 1, 1, 2)
            elif __command__[1] == "d":
                bitblt(stdscr, _screens_["delay"]["1"], _screens_["size"]["width"], 1, 1, 2)
                time.sleep(0.25)
                bitblt(stdscr, _screens_["delay"]["2"], _screens_["size"]["width"], 1, 1, 2)
                time.sleep(0.25)
                bitblt(stdscr, _screens_["delay"]["3"], _screens_["size"]["width"], 1, 1, 2)
                time.sleep(0.5)
        else:
            pass


def start_loop(stdscr):
    global __thread__
    global __execute__
    global __command__
    __command__ = None
    __execute__ = True
    __thread__ = threading.Thread(target=__switcher__, args=(stdscr,))
    __thread__.setDaemon(True)
    __thread__.start()


def stop_loop():
    global __execute__
    __execute__ = False


def init_screen(stdscr):
    __init_color__()
    stdscr.clear()


def update_command(obj):
    global __command__
    __command__ = obj


def init(callable_obj, screens_obj):
    global _screens_
    _screens_ = screens_obj
    curses.wrapper(callable_obj)
