from __future__ import print_function

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString

# -----------------------------------------------------------------------------------------

t_pinhole_x = 5.
t_pinhole_y = 97.

f_pinhole_x = 109.
f_pinhole_y = 0.

b_pinhole_x = 5. + 102 * np.cos(np.radians(-82.5))
b_pinhole_y = 102.0 * np.sin(np.radians(-82.5))

print('t_pinhole_x:', t_pinhole_x)
print('t_pinhole_y:', t_pinhole_y)

print('f_pinhole_x:', f_pinhole_x)
print('f_pinhole_y:', f_pinhole_y)

print('b_pinhole_x:', b_pinhole_x)
print('b_pinhole_y:', b_pinhole_y)

# -----------------------------------------------------------------------------------------

n = 16              # number of detectors per camera
size = 0.75         # detector size
space = 0.2         # space between detectors
step = size+space   # distance between the centers of adjacent detectors

t_dist = 9.     # distance from camera to pinhole
f_dist = 9.
b_dist = 13.

t_theta = np.pi                 # Top: rotated 180deg (upside down)
f_theta = np.pi / 2.            # Front: vertical on the LFS (facing left) 90deg
b_theta = np.pi * 7.5 / 180.    # Bottom: looking up at slight positive angle 7.5deg

# ----------------------------------------------------------------------------------------

##########################################################################################
#                                   TOP                                                  #
##########################################################################################
# Pinhole frame of reference
t_detector_x = np.linspace(-1., 1., n) * step * (n - 1.) / 2.
t_detector_y = - np.ones(n) * t_dist

# Rotation and translation to the tokamak frame of reference
t_detector_rotated_x = t_detector_x*np.cos(t_theta) - t_detector_y*np.sin(t_theta)
t_detector_rotated_y = t_detector_x*np.sin(t_theta) + t_detector_y*np.cos(t_theta)
t_detector_x = t_pinhole_x + t_detector_rotated_x
t_detector_y = t_pinhole_y + t_detector_rotated_y

##########################################################################################
#                                   FRONT                                                #
##########################################################################################
# Pinhole frame of reference
f_detector_x = np.linspace(-1., 1., n) * step * (n - 1.) / 2.
f_detector_y = - np.ones(n) * f_dist

# Rotation and translation to the tokamak frame of reference
f_detector_rotated_x = f_detector_x*np.cos(f_theta) - f_detector_y*np.sin(f_theta)
f_detector_rotated_y = f_detector_x*np.sin(f_theta) + f_detector_y*np.cos(f_theta)
f_detector_x = f_pinhole_x + f_detector_rotated_x
f_detector_y = f_pinhole_y + f_detector_rotated_y

##########################################################################################
#                                   BOTTOM                                               #
##########################################################################################
# Pinhole frame of reference
b_detector_x = np.linspace(-1., 1., n) * step * (n - 1.) / 2.
b_detector_y = - np.ones(n) * b_dist

# Rotation and translation to the tokamak frame of reference
b_detector_rotated_x = b_detector_x*np.cos(b_theta) - b_detector_y*np.sin(b_theta)
b_detector_rotated_y = b_detector_x*np.sin(b_theta) + b_detector_y*np.cos(b_theta)
b_detector_x = b_pinhole_x + b_detector_rotated_x
b_detector_y = b_pinhole_y + b_detector_rotated_y

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

for (i, row) in enumerate(df.itertuples()):
    if i < n:
        color = 'darkturquoise'
    elif i < 2*n:
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

plt.title('cameras')

plt.show()
