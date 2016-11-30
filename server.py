#!/usr/bin/python3
import output_modules.curses as display  # can change the output mode
import json
import signal
import paho.mqtt.client as mqtt
global sceens
screens = json.load(open("screens.json"))
IP = '127.0.0.1'
TOPIC = 'drones/drone1'


def on_message(client, userdata, message):
    global scrstd
    message = message.payload
    try:                                                      # if bytes,
        display.update_command([scrstd, decodebin(message)])  # we display it;
    except TypeError:                                         # if that fails,
        display.update_command([scrstd, get(message)])        # we use the dict
    except:
        client.publish(TOPIC, "FAIL")
    else:
        client.publish(TOPIC, "ACK")


def get(name):
    global screens
    name=str(name, "utf8")
    if len(name) == 1:  # if it's a kernel hook,
        return name     # it will be sent verbatim
    split = name.split("/")
    if len(split) == 1:                       # if it's an emotion name,
        return screens['emotions'][split[0]]  # it's in the emotions dict
    elif len(split) == 2:                     # if it's a path,
        return screens[split[0]][split[1]]    # we include it into the lookup


def decodebin(binar, outlen):
    if not isinstance(binar, bytes):                       # if not bytes,
        raise TypeError("Expected bytes, but got " + str(  # complaining ensues
            type(binar)).split("'")[1])
    return list(bin(int(binar.hex(), 16))[2:][:outlen])    # that's the parser


def init(stdscr):
    if stdscr is not None:
        display.init_screen(stdscr)
    global scrstd
    scrstd = stdscr
    global m
    m = mqtt.Client()
    m.connect(IP)
    m.subscribe(TOPIC)
    m.on_message = on_message
    m.loop_start()
    display.start_loop(stdscr)
    display.update_command("d")
    signal.pause()

if __name__ == '__main__':
    display.init(init, json.load(open("screens.json")))
