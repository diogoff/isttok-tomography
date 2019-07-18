from __future__ import print_function

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString

# -----------------------------------------------------------------------------------------

v_pinhole_x = 5.
v_pinhole_y = 97.

h_pinhole_x = 109.
h_pinhole_y = 0.

print('v_pinhole_x:', v_pinhole_x)
print('v_pinhole_y:', v_pinhole_y)

print('h_pinhole_x:', h_pinhole_x)
print('h_pinhole_y:', h_pinhole_y)

# -----------------------------------------------------------------------------------------

n = 16               # number of detectors per camera
size = 0.75          # detector size
space = 0.2          # space between detectors
step = size + space  # distance between the centers of adjacent detectors

v_dist = 9.          # distance from camera to pinhole
h_dist = 9.

v_theta = np.pi      # vertical camera: rotated 180 degrees from bottom
h_theta = np.pi / 2. # horizontal camera: rotated 90 degrees from bottom

# ----------------------------------------------------------------------------------------

# pinhole frame of reference
v_detector_x = np.linspace(1., -1., n) * step * (n-1.)/2.
v_detector_y = (-1.) * np.ones(n) * v_dist

# rotation
v_detector_rotated_x = v_detector_x*np.cos(v_theta) - v_detector_y*np.sin(v_theta)
v_detector_rotated_y = v_detector_x*np.sin(v_theta) + v_detector_y*np.cos(v_theta)

# translation to the vessel frame of reference
v_detector_x = v_pinhole_x + v_detector_rotated_x
v_detector_y = v_pinhole_y + v_detector_rotated_y

# calibration factors (etendue)
v_etendue = [0.03155177, 0.04362264, 0.05633366, 0.06869239,
             0.09645432, 0.11267896, 0.12971384, 0.14767003,
             0.15017711, 0.14139539, 0.12288025, 0.10543017,
             0.08804052, 0.06193492, 0.05265601, 0.05495817]

print('v_detector_x:', v_detector_x)
print('v_detector_y:', v_detector_y)

# ----------------------------------------------------------------------------------------

# pinhole frame of reference
h_detector_x = np.linspace(1., -1., n) * step * (n-1.)/2.
h_detector_y = (-1.) * np.ones(n) * h_dist

# rotation
h_detector_rotated_x = h_detector_x*np.cos(h_theta) - h_detector_y*np.sin(h_theta)
h_detector_rotated_y = h_detector_x*np.sin(h_theta) + h_detector_y*np.cos(h_theta)

# translation to the vessel frame of reference
h_detector_x = h_pinhole_x + h_detector_rotated_x
h_detector_y = h_pinhole_y + h_detector_rotated_y

# calibration factors (etendue)
h_etendue = [0.00210049, 0.00611418, 0.01208648, 0.01871730,
             0.02721384, 0.03679548, 0.04456807, 0.05030524,
             0.05118717, 0.04779802, 0.04111613, 0.03216692,
             0.02290661, 0.01593762, 0.01080871, 0.00883411]

print('h_detector_x:', h_detector_x)
print('h_detector_y:', h_detector_y)

# -----------------------------------------------------------------------------------------

coords = []

for i in range(n):
    x0 = v_detector_x[i]
    y0 = v_detector_y[i]
    x1 = v_pinhole_x
    y1 = v_pinhole_y
    m = (y1-y0)/(x1-x0)
    b = (y0*x1-y1*x0)/(x1-x0)
    y2 = -100.
    x2 = (y2-b)/m
    line = LineString([(x0, y0), (x2, y2)])
    circle = Point(0., 0.).buffer(100.).boundary
    segment = line.difference(circle)[1]
    x0, y0 = segment.coords[0]
    x1, y1 = segment.coords[1]
    camera = 'vertical'
    print('%10s %10.6f %10.6f %10.6f %10.6f %10.6f' % (camera, x0, y0, x1, y1, v_etendue[i]))
    coords.append([camera, x0, y0, x1, y1, v_etendue[i]])

for i in range(n):
    x0 = h_detector_x[i]
    y0 = h_detector_y[i]
    x1 = h_pinhole_x
    y1 = h_pinhole_y
    m = (y1-y0)/(x1-x0)
    b = (y0*x1-y1*x0)/(x1-x0)
    x2 = -100.
    y2 = m*x2+b
    line = LineString([(x0, y0), (x2, y2)])
    circle = Point(0., 0.).buffer(100.).boundary
    segment = line.difference(circle)[1]
    x0, y0 = segment.coords[0]
    x1, y1 = segment.coords[1]
    camera = 'horizontal'
    print('%10s %10.6f %10.6f %10.6f %10.6f %10.6f' % (camera, x0, y0, x1, y1, h_etendue[i]))
    coords.append([camera, x0, y0, x1, y1, h_etendue[i]])

# -----------------------------------------------------------------------------------------

df = pd.DataFrame(coords, columns=['camera', 'x0', 'y0', 'x1', 'y1', 'etendue'])

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
