#!/usr/bin/env python
import sys, os
from PIL import Image
from colorsys import hls_to_rgb, rgb_to_hls
import numpy as np
from math import sqrt, floor

def dist(p1,p2):
    return sqrt(sum((p1 - p2) ** 2))

rgb2hex = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))
darken = lambda rgb : (p * gamma for p in rgb)

filename = sys.argv[1] 

colors = np.array([
        [0,0,0],
        [170,0,0],
        [0,170,0],
        [220,155,0],
        [0,0,170],
        [170,0,170],
        [0,170,170],
        [170,170,170],
        [85,85,85],
        [255,0,0],
        [85,255,85],
        [255,255,0],
        [85,85,255],
        [255,85,255],
        [85,255,255],
        [255,255,255]
    ])
    
nns = [[np.array([]), 0xFFFFFFFF]]*len(colors)

img = Image.open(filename)
img.thumbnail((img.width/10,img.height/10))
pixels = np.array(img)

for row in pixels:
    for p in row:
        for i in range(len(colors)):
            d = dist(p[:3], colors[i])
            if d < nns[i][1]:
                nns[i] = [p, d]

# for i in range(len(colors)):
    # nns[i][0] = ( colors[i] + (nns[i][0] * 2) ) // 3
    
for nn in nns:
    print(rgb2hex(nn[0][:3]))
    
print(rgb2hex(pixels.mean(axis=1).mean(axis=0, dtype=int)))
    



# rgbs = [map(int, c) for c in kmeans.cluster_centers_]

# write = sys.stdout.write
# for i in range(0, nbrcentroids):
#     write('\033[0;3%dm ' % i)
# write('\n')