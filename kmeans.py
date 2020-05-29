#!/usr/bin/python3
import numpy as np
import sys
import os
from PIL import Image
from colorsys import hsv_to_rgb, rgb_to_hsv

ANSI = np.array(
    [ 
        [0,0,0],
        [255,0,0],
        [0,255,0],
        [255,128,0],
        [0,0,255],
        [255,0,255],
        [0,255,255],
        [255,255,255],
    ]
)

try:
    wp_path = sys.argv[1] if sys.argv[1] else eval('raise ValueError')
except:
    with open(f"{os.environ['HOME']}/.config/nitrogen/bg-saved.cfg", 'r') as wp_file:
        wp_file.readline()
        wp_path = wp_file.readline().split('=')[1].strip()
try:
    iterations = int(sys.argv[2])
except:
    iterations = 4
    
wp=Image.open(wp_path).convert('RGB')
wp.thumbnail((500, 500), resample=Image.LANCZOS)
pixels=np.array(wp, dtype=int)[:,:,:3]
pixels=pixels.reshape(pixels.shape[0] * pixels.shape[1], pixels.shape[2])


closest_pixel_index_per_ANSI = np.argmin(
    (
        (
            ANSI - pixels[:, np.newaxis]
        )**2
    ).sum(axis=2)
    , axis=0
)

closest_pixel_to_each_ANSI  = np.array([pixels[closest_pixel_index_per_ANSI[k]] for k in range(ANSI.shape[0])])

centroids = closest_pixel_to_each_ANSI.copy()

for i in range(iterations):

    # centroids = (centroids + ANSI)/2
    closest_cluster_index_per_pixel = np.argmin(
        (
            (
                pixels - centroids[:, np.newaxis]
            )**2
        ).sum(axis=2)
        , axis=0
    )
        
    closest_pixels_to_each_ANSI = np.array(
        [
            pixels[closest_cluster_index_per_pixel==k] 
            for k in range(ANSI.shape[0])
        ]
    )

    centroids = np.array(
        [
            m.mean(axis=0) for m in [
                np.concatenate([
                    closest_pixels_to_each_ANSI[nli],
                    closest_pixel_to_each_ANSI[nli][np.newaxis]
                ])
                for nli in range(closest_pixels_to_each_ANSI.shape[0])
            ]
        ]
    )
    
    centroids = (19 * centroids + ANSI)/20

hsvs = np.array(list(map(lambda c: rgb_to_hsv(*c), centroids)))
hsvs[:,2]=np.minimum(hsvs[:,2]*1.5, np.repeat(255, hsvs.shape[0]))
hsvs[0,2]*=1.5
brights=np.array(list(map(lambda c: hsv_to_rgb(*c), hsvs)))

try:
    sys.argv[3]
    hsvs = np.array(list(map(lambda c: rgb_to_hsv(*c), centroids)))
    hsv_nonbinary = hsvs[1:-2]
    hsv_nonbinary[:,2]=np.minimum(hsv_nonbinary[:,2]/1.1, np.repeat(255, hsv_nonbinary.shape[0]))
    hsv_nonbinary[:,1]=np.minimum(hsv_nonbinary[:,1]*2, np.repeat(255, hsv_nonbinary.shape[0]))
    light_colors=np.array(list(map(lambda c: hsv_to_rgb(*c), hsvs))).clip(0,255)

    # Swap black and white
    # light_colors[[0, -1]] = light_colors[[-1, 0]]
    light_colors[0] = brights[-1]
    light_colors[-1] = centroids[0]
    
    centroids[[0, -1]] = centroids[[-1, 0]]
    centroids[0] = brights[-1]
    brights=light_colors
except:
    pass

avg_color = np.array(list(map(int, pixels.mean(axis=0))))

# avg_color = pixels.mean(axis=0)

def luminanace(rgb):
    rgb /= 255
    l=[c/ 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return l[0] * 0.2126 + l[1] * 0.7152 + l[2] * 0.0722;

def contrast(rgb1, rgb2):
    return (luminanace(rgb1)+ 0.05) / (luminanace(rgb2) + 0.05);

palette=np.concatenate([centroids, brights]).clip(0,255)
cs=[list(map(int,c)) for c in palette]
print("\n".join(["color%d #%02x%02x%02x" % (i, *c) for i,c in enumerate(cs) ]))
print("\n".join(["color%d \x1b[48;2;%d;%d;%dm#%02x%02x%02x\x1b[0m" % (i, *c, *c) for i,c in enumerate(cs) ]), file=sys.stderr)
# print(avg_color, file=sys.stderr)
print("average \x1b[48;2;%d;%d;%dm#%02x%02x%02x\x1b[0m" % (*avg_color, *avg_color), file=sys.stderr)
# print(contrast(avg_color, centroids[0]), file=sys.stderr)
# print(contrast(brights[7], avg_color), file=sys.stderr)
