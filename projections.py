from __future__ import print_function

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import MultiLineString, LineString

# -----------------------------------------------------------------------------------------

fname = 'cameras.csv'
print('Reading:', fname)
df = pd.read_csv(fname)

print(df)

# -----------------------------------------------------------------------------------------

n_rows = 15   # y-axis pixel resolution
n_cols = 15   # x-axis pixel resolution

x_min = -100.
x_max = +100.

y_min = -100.
y_max = +100.


def transform(x, y):
    j = int((x-x_min)/(x_max-x_min)*n_cols)
    i = int((y_max-y)/(y_max-y_min)*n_rows)
    return (i, j)

# -------------------------------------------------------------------------

x_grid = np.linspace(x_min, x_max, num=n_cols+1)
y_grid = np.linspace(y_min, y_max, num=n_rows+1)

grid = []

for x in x_grid:
    grid.append([(x, y_min), (x, y_max)])

for y in y_grid:
    grid.append([(x_min, y), (x_max, y)])

grid = MultiLineString(grid)

# -------------------------------------------------------------------------

projections = []

for row in df.itertuples():
    line = LineString([(row.x0, row.y0), (row.x1, row.y1)])
    projection = np.zeros((n_rows, n_cols))
    for segment in line.difference(grid):
        xx, yy = segment.xy
        x_mean = np.mean(xx)
        y_mean = np.mean(yy)
        (i, j) = transform(x_mean, y_mean)
        projection[i,j] = segment.length
    projections.append(projection * row.etendue)
    
projections = np.array(projections)

print('projections:', projections.shape, projections.dtype)

# -------------------------------------------------------------------------

fname = 'projections.npy'
print('Writing:', fname)
np.save(fname, projections)

# -------------------------------------------------------------------------

vmin = 0.
vmax = np.max([projections[k] for k in df[df['camera']=='vertical'].index])

ni = 4
nj = 4
figsize = (2*nj, 2*ni)

fig, ax = plt.subplots(ni, nj, figsize=figsize)
for i in range(ni):
    for j in range(nj):
        k = i*nj + j
        ax[i,j].imshow(projections[k], vmin=vmin, vmax=vmax)
        ax[i,j].set_axis_off()

fig.suptitle('projections (vertical camera)')
plt.show()

# -------------------------------------------------------------------------

vmin = 0.
vmax = np.max([projections[k] for k in df[df['camera']=='horizontal'].index])

fig, ax = plt.subplots(ni, nj, figsize=figsize)
for i in range(ni):
    for j in range(nj):
        k = i*nj + j + ni*nj
        ax[i,j].imshow(projections[k], vmin=vmin, vmax=vmax)
        ax[i,j].set_axis_off()

fig.suptitle('projections (horizontal camera)')
plt.show()
