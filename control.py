#!/usr/bin/python3
import tkinter
import paho.mqtt.client as mqtt
import json
m = mqtt.Client()
m.connect("127.0.0.1")
root = tkinter.Tk()
screens = json.load(open("screens.json"))


class Executer:
    def null(self):
        pass
    def __init__(self, target=None, param=None):
        if target:
            self.target = target
            self.param = param
        else:
            self.target = self.null
    def __call__(self):
        if self.param:
            self.target(self.param)
        else:
            self.target()

def send(obj):
    global m
    m.publish("drones/drone1", payload=obj)
functs = {"Pause":Executer(target=send, param="d"), "QUIT":Executer(target=send, param="Q")}
for i in screens["emotions"]:
    functs.update({i:Executer(target=send, param=i)})
buts = {}
for i in sorted(list(functs)):
    o=tkinter.Button(root, text=i, command=functs[i])
    o.pack()
    buts.update({i:o})
root.mainloop()

