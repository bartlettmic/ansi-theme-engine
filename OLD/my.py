#!/usr/bin/python3
from PIL import Image
from sys import argv
from colorsys import hls_to_rgb, rgb_to_hls
import numpy as np

from math import sqrt, floor
def dist(p1,p2):
    return sqrt(sum((np.array(p1) - np.array(p2)) ** 2))
    
COLORS=6
COLOR_STEP=1/COLORS
hue = 0
rgbs = [[255,255,255],[0,0,0]]

for i in range(COLORS):
    rgbs.append([int(c*255) for c in hls_to_rgb(hue, 0.5, 1.0)])
    hue = hue + COLOR_STEP
    
img_path = argv[1]
img = Image.open(img_path)
img.thumbnail((100, 100))
pixels = np.array(img)

w, h = img.size
matrix = np.zeros(img.size)
clusters = np.array([[[]]]*(COLORS+2))

print(clusters)

for x in range(w):
    for y in range(h):
        mindex=0
        mindist=float('Inf')
        for i in range(len(rgbs)):
            this_dist = dist(rgbs[i],pixels[x,y])
            if this_dist < mindist:
                mindist = this_dist
                mindex = i
        # clusters[mindex].append(pixels[x,y])
        np.append(clusters[mindex], pixels[x,y])

# for count, color in img.getcolors(w * h):
    # print(count, color)
    

    
exit(0)
    
just_rgb = [map(float, c[1]) for c in colors ]

hues = list(map(lambda c: rgb_to_hls(*c), just_rgb))
hues.sort(key=lambda c: c[0])
hues = list(map(lambda c: hls_to_rgb(*c), hues))

print(hues)