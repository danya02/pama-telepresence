#!/usr/bin/python3
import subprocess
import pygame
import pygame.image
import time
import threading


def chunks(l, n):
    return list(zip(*[iter(l)]*n))


def _update_screen_(surface):
    pygame.image.save(surface, "/tmp/pama-face.png")
    global _display_program_
    try:
        _display_program_.terminate()
    except:
        pass
    _display_program_ = subprocess.Popen(["fbi", "-a", "/tmp/pama-face.png"])


def bitblt(null, screen, width, intrue, outtrue, outfalse):
    screen = chunks(screen, width)
    truecolor = pygame.Color(outtrue)
    falsecolor = pygame.Color(outfalse)
    surface = pygame.Surface((width, len(screen[0])))
    for j, k in zip(screen, range(len(screen))):
        for l, m in zip(j, range(len(j))):
            surface.set_at((m, k), truecolor if l == intrue else falsecolor)
    _update_screen_(surface)


def __switcher__():
    global __command__
    global _screens_
    global __execute__
    while __execute__:
        if isinstance(__command__, list):
            if isinstance(__command__[1], list):
                bitblt(__command__[0], __command__[1], _screens_["size"]["width"], 1, "#00ff00", "#000000")
            elif __command__[1] == "d":
                bitblt(None, _screens_["delay"]["1"], _screens_["size"]["width"], 1, "#00ff00", "#000000")
                time.sleep(0.25)
                bitblt(None, _screens_["delay"]["2"], _screens_["size"]["width"], 1, "#00ff00", "#000000")
                time.sleep(0.25)
                bitblt(None, _screens_["delay"]["3"], _screens_["size"]["width"], 1, "#00ff00", "#000000")
                time.sleep(0.5)
        else:
            pass


def start_loop(stdscr):
    global __thread__
    global __execute__
    global __command__
    __command__ = None
    __execute__ = True
    __thread__ = threading.Thread(target=__switcher__)
    __thread__.setDaemon(True)
    __thread__.start()


def stop_loop():
    global __execute__
    __execute__ = False


def init_screen(stdscr):
    pass


def update_command(obj):
    global __command__
    __command__ = obj


def init(callable_obj, screens_obj):
    global _screens_
    _screens_ = screens_obj
    callable_obj(None)
