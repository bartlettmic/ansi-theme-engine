#!/usr/bin/python3

from numpy import array
from math import sqrt, floor
from colorsys import hls_to_rgb, rgb_to_hls


def dist(p1,p2):
    return sqrt(sum((p1 - p2) ** 2))
    
COLORS=6
COLOR_STEP=1/COLORS
hue = 0

for i in range(COLORS):
    print(
        f"""rgb({
            ','.join(
                map(str,
                    [int(c*255) for c in hls_to_rgb(
                                            hue, 0.5, 1.0
                                                )]
                )
            )
        })"""
    )
    hue = hue + COLOR_STEP

