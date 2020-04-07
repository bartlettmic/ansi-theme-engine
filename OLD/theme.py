#!/usr/bin/env python3
import fileinput

# from sys import argv
# import subprocess

# cmd = "export `cat ~/.config/nitrogen/bg-saved.cfg | grep file` ; convert $file -dither Riemersma -colors 16 -unique-colors -format "%c" histogram:info:"
# password = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')

def cprint(c):
    print(f"rgb{c}")

from colorsys import hls_to_rgb, rgb_to_hls
from ast import literal_eval

colors = []

for line in fileinput.input():
    line=line.replace(' ','')
    line = line.split(':')[1].split("#")[0]
    line = literal_eval(line)
    colors.append((line[0],line[1],line[2]))
    
subcolors = colors[1:-1] # 0=black, -1=white

for c in colors:
    cprint(c)
    
print()

hues = list(map(lambda c: rgb_to_hls(*c), subcolors))
hues.sort(key=lambda c: c[0])
hues = list(map(lambda c: hls_to_rgb(*c), hues))

cprint(colors[0])
for c in hues:
    cprint(tuple(map(int,c)))
cprint(colors[-1])

# ~(themer) /opt/themer > export "`cat ~/.config/nitrogen/bg-saved.cfg | grep file`" ; convert $file -scale 50x50! -depth 8 +dither -colors 16 -format "%c" histogram:info: | ~/Desktop/theme.py | clip

"""
black
red
yellow
green
cyan
blue
magenta
white
"""
