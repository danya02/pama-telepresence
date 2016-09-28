#!/usr/bin/python3
import curses
import json
import argparse
import time


def parse_cmd_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("script", type=str,
                        help="execute sequence of commands")
    comms = parser.parse_args()
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
                    commands += [dataset["delay"][i]]
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
    init_color()
    stdscr.clear()
    comms, screens = parse_cmd_line()
    commands = parse(comms.script.split(" "), screens)
    for i in commands:
        if isinstance(i, float):
            time.sleep(i)
        if isinstance(i, list):
            bitblt(stdscr, i, screens["size"]["width"], 1, 1, 2)
if __name__ == "__main__":
    curses.wrapper(main)
