#!/usr/bin/python3
import curses
import json
import argparse
import time
import threading


def parse_cmd_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("script", type=str,
                        help="execute sequence of commands")
    comms = parser.parse_args()
    global screens
    screens = json.load(open("screens.json"))
    return comms, screens


def chunks(l, n):
    return list(zip(*[iter(l)]*n))


def bitblt(stdscr, screen, width, intrue, outtrue, outfalse):
    screen = chunks(screen, width)
    for j, k in zip(screen, range(len(screen))):
        for l, m in zip(j, range(len(j))):
            m = m*2
            stdscr.addstr(k, m, "  ", curses.color_pair(outtrue if l == intrue else outfalse))
    stdscr.refresh()


def switcher():
    global switching_command
    global screens
    while 1:
        if isinstance(switching_command, list):
            if isinstance(switching_command[1], list):
                bitblt(switching_command[0], switching_command[1], screens["size"]["width"], 1, 1, 2)
            elif switching_command[1] == "d":
                bitblt(switching_command[0], screens["delay"]["1"], screens["size"]["width"], 1, 1, 2)
                time.sleep(0.25)
                bitblt(switching_command[0], screens["delay"]["2"], screens["size"]["width"], 1, 1, 2)
                time.sleep(0.25)
                bitblt(switching_command[0], screens["delay"]["3"], screens["size"]["width"], 1, 1, 2)
                time.sleep(0.5)
        else:
            pass


def parse(script, dataset):
    commands = []
    result = 0
    for i in script:
        try:
            commands += [float(i.split("d")[1])]
            result += 1
        except:
            try:
                commands += [dataset["emotions"][i]]
                result += 1
            except:
                try:
                    assert(i == "p")
                    commands += "d"
                    result += 1
                except:
                    pass
    if not result == len(script):
        raise ValueError("Error in script")
    else:
        return commands


def init_color():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)


def main(stdscr):
    global switching_command
    switching_command = None
    switch = threading.Thread(target=switcher)
    switch.setDaemon(True)
    switch.start()
    init_color()
    stdscr.clear()
    comms, screens = parse_cmd_line()
    commands = parse(comms.script.split(" "), screens)
    for i in commands:
        if isinstance(i, float):
            time.sleep(i)
        elif isinstance(i, list):
            switching_command = [stdscr, i]
        elif i == "d":
            switching_command = [stdscr, "d"]
if __name__ == "__main__":
    curses.wrapper(main)
