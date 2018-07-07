from __future__ import print_function

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString

# -----------------------------------------------------------------------------------------

t_pinhole_x = 5.
t_pinhole_y = 104.

f_pinhole_x = 104.
f_pinhole_y = 0.

b_pinhole_x = 5.
b_pinhole_y = -104.

print('t_pinhole_x:', t_pinhole_x)
print('t_pinhole_y:', t_pinhole_y)

print('f_pinhole_x:', f_pinhole_x)
print('f_pinhole_y:', f_pinhole_y)

print('b_pinhole_x:', b_pinhole_x)
print('b_pinhole_y:', b_pinhole_y)

# -----------------------------------------------------------------------------------------

n = 8
pixel = 1.5
space = 10./18.
dist = 10.

t_detector_x = t_pinhole_x - (n*pixel + (n-1)*space)/2. + pixel/2. + np.arange(n)*(pixel + space)
t_detector_y = (t_pinhole_y + dist) * np.ones(n)

f_detector_x = (f_pinhole_x + dist) * np.ones(n)
f_detector_y = f_pinhole_y + (n*pixel + (n-1)*space)/2. - pixel/2. - np.arange(n)*(pixel + space)

b_detector_x = b_pinhole_x + (n*pixel + (n-1)*space)/2. - pixel/2. - np.arange(n)*(pixel + space)
b_detector_y = (b_pinhole_y - dist) * np.ones(n)

print('t_detector_x:', t_detector_x)
print('t_detector_y:', t_detector_y)

print('f_detector_x:', f_detector_x)
print('f_detector_y:', f_detector_y)

print('b_detector_x:', b_detector_x)
print('b_detector_y:', b_detector_y)

# -----------------------------------------------------------------------------------------

coords = []

for i in range(n):
    x0 = t_detector_x[i]
    y0 = t_detector_y[i]
    x1 = t_pinhole_x
    y1 = t_pinhole_y
    m = (y1-y0)/(x1-x0)
    b = (y0*x1-y1*x0)/(x1-x0)
    y2 = -100.
    x2 = (y2-b)/m
    line = LineString([(x0, y0), (x2, y2)])
    circle = Point(0., 0.).buffer(100.).boundary
    segment = line.difference(circle)[1]
    x0, y0 = segment.coords[0]
    x1, y1 = segment.coords[1]
    print('%10s %10.6f %10.6f %10.6f %10.6f' % ('top', x0, y0, x1, y1))
    coords.append(['top', x0, y0, x1, y1])

for i in range(n):
    x0 = f_detector_x[i]
    y0 = f_detector_y[i]
    x1 = f_pinhole_x
    y1 = f_pinhole_y
    m = (y1-y0)/(x1-x0)
    b = (y0*x1-y1*x0)/(x1-x0)
    x2 = -100.
    y2 = m*x2+b
    line = LineString([(x0, y0), (x2, y2)])
    circle = Point(0., 0.).buffer(100.).boundary
    segment = line.difference(circle)[1]
    x0, y0 = segment.coords[0]
    x1, y1 = segment.coords[1]
    print('%10s %10.6f %10.6f %10.6f %10.6f' % ('front', x0, y0, x1, y1))
    coords.append(['front', x0, y0, x1, y1])

for i in range(n):
    x0 = b_detector_x[i]
    y0 = b_detector_y[i]
    x1 = b_pinhole_x
    y1 = b_pinhole_y
    m = (y1-y0)/(x1-x0)
    b = (y0*x1-y1*x0)/(x1-x0)
    y2 = 100.
    x2 = (y2-b)/m
    line = LineString([(x0, y0), (x2, y2)])
    circle = Point(0., 0.).buffer(100.).boundary
    segment = line.difference(circle)[1]
    x0, y0 = segment.coords[0]
    x1, y1 = segment.coords[1]
    print('%10s %10.6f %10.6f %10.6f %10.6f' % ('bottom', x0, y0, x1, y1))
    coords.append(['bottom', x0, y0, x1, y1])

# -----------------------------------------------------------------------------------------

df = pd.DataFrame(coords, columns=['camera', 'x0', 'y0', 'x1', 'y1'])

fname = 'cameras.csv'
print('Writing:', fname)
df.to_csv(fname, index=False)

# -----------------------------------------------------------------------------------------

fname = 'cameras.csv'
print('Reading:', fname)
df = pd.read_csv(fname)

print(df)

# -----------------------------------------------------------------------------------------

for (i, row) in enumerate(df.itertuples()):
    if i < 8:
        color = 'darkturquoise'
    elif i < 16:
        color = 'limegreen'
    else:
        color = 'orange'
    plt.plot([row.x0, row.x1], [row.y0, row.y1], color)

circle = plt.Circle((0., 0.), 100., color='k', fill=False)
plt.gca().add_artist(circle)

plt.plot(0., 0., 'k+')

plt.gca().set_aspect('equal')

plt.xlabel('x (mm)')
plt.ylabel('y (mm)')

plt.title('lines of sight')

plt.show()
