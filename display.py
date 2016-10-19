#!/usr/bin/python3
import json
import argparse
import time
import output_modules.curses as output


def parse_cmd_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("script", type=str,
                        help="execute sequence of commands")
    comms = parser.parse_args()
    global screens
    screens = json.load(open("screens.json"))
    return comms, screens


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


def main(stdscr):
    output.init_screen()
    output.start_loop(stdscr)
    comms, screens = parse_cmd_line()
    commands = parse(comms.script.split(" "), screens)
    for i in commands:
        if isinstance(i, float):
            time.sleep(i)
        elif isinstance(i, list):
            output.update_command([stdscr, i])
        elif i == "d":
            output.update_command([stdscr, "d"])
if __name__ == "__main__":
    output.init(main, json.load(open("screens.json")))
