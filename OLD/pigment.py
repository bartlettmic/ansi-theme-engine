#!/usr/bin/env python
import sys, os
from sklearn.cluster import KMeans
from PIL import Image

nbrcentroids = int(sys.argv[2]) or 10
beta = 10
gamma = 0.4
rgb2hex = lambda rgb: '#%s' % ''.join(('%02x' % min(p + beta, 255) for p in rgb))
darken = lambda rgb : (p * gamma for p in rgb)

def getcentroids(filename, n=8):
    img = Image.open(filename)
    img.thumbnail((100, 100))
    kmeans = KMeans(init='k-means++', n_clusters=n)
    kmeans.fit(list(img.getdata()))
    # return kmeans.cluster_centers_
    # rgbs = [map(int, c) for c in kmeans.cluster_centers_]
    rgbs = [ [ int(c) for c in p ] for p in kmeans.cluster_centers_]
    return rgbs

def print_colors(centroids):
    centroids = sorted(centroids, key=lambda rgb: sum(c**2 for c in rgb))
    for c in centroids:
        print(f"\x1b[48;2;{c[0]};{c[1]};{c[2]}m{rgb2hex(c)}\x1b[0m")

centroids = getcentroids(sys.argv[1], n=nbrcentroids)
print_colors(centroids)
