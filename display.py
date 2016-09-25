#!/usr/bin/python3
import curses
import json
import argparse
import random
import time
parser=argparse.ArgumentParser()
parser.add_argument("script", type=str, help="execute sequence of commands")
comms=parser.parse_args()
screens=json.load(open("screens.json"))
def chunks(l, n):
	return list(zip(*[iter(l)]*n))
def main(stdscr):
	curses.start_color()
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
	scr=comms.script.split(" ")
	commands=[]
	result=0
	for i in scr:
		try:
			commands+=[float(i.split("d")[1])]
			result+=1
		except:
			try:
				commands+=[screens["emotions"][i]]
				result+=1
			except:
				try:
					commands+=[screens["delay"][i]]
					result+=1
				except:
					pass
	if not result==len(scr):
		raise ValueError("Error in script")
	stdscr.clear()
	for i in commands:
		if isinstance(i, float):
			#stdscr.getkey()
			time.sleep(1)
		items=""
		if isinstance(i, list):
			i=chunks(i, screens["size"]["width"])
			for j,k in zip(i, range(len(i))):
				for l,m in zip(j, range(len(j))):
					m=m*2
					items+=str(l)
#					j=random.randint(0,1)
					stdscr.addstr(k,m, "  ", curses.color_pair(2 if l==0 else 1))
			open("/tmp/output_list.txt","w").write(items)
			stdscr.refresh()
			#stdscr.getkey()
curses.wrapper(main)
