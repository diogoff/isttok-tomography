from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------------------------

fname = 'projections.npy'
print('Reading:', fname)
projections = np.load(fname)

print('projections:', projections.shape, projections.dtype)

# -------------------------------------------------------------------------

fname = 'signals_data.npy'
print('Reading:', fname)
signals_data = np.load(fname)

print('signals_data:', signals_data.shape, signals_data.dtype)

fname = 'signals_time.npy'
print('Reading:', fname)
signals_time = np.load(fname)

print('signals_time:', signals_time.shape, signals_time.dtype)

# -------------------------------------------------------------------------

P = projections.reshape((projections.shape[0], -1))

print('P:', P.shape, P.dtype)

# -------------------------------------------------------------------------

n_rows = projections.shape[1]
n_cols = projections.shape[2]

Dh = np.eye(n_rows*n_cols) - np.roll(np.eye(n_rows*n_cols), -1, axis=1)
Dv = np.eye(n_rows*n_cols) - np.roll(np.eye(n_rows*n_cols), -n_cols, axis=1)

print('Dh:', Dh.shape, Dh.dtype)
print('Dv:', Dv.shape, Dv.dtype)

# -------------------------------------------------------------------------

Pt = np.transpose(P)
PtP = np.dot(Pt, P)

DtDh = np.dot(np.transpose(Dh), Dh)
DtDv = np.dot(np.transpose(Dv), Dv)

alpha = 1e2

inv = np.linalg.inv(PtP + alpha*(DtDh + DtDv))

M = np.dot(inv, Pt)

# -------------------------------------------------------------------------

tomo = []
tomo_t = np.arange(0., signals_time[0,-1], 0.005)

for t in tomo_t:
    i = np.argmin(np.fabs(signals_time[0] - t))
    f = signals_data[:,i].reshape((-1, 1))
    g = np.dot(M, f)
    tomo.append(g.reshape((n_rows, n_cols)))

tomo = np.array(tomo)

print('tomo:', tomo.shape, tomo.dtype)
print('tomo_t:', tomo_t.shape, tomo_t.dtype)

# -------------------------------------------------------------------------

vmin = 0.
vmax = np.max(tomo)

ni = 4
nj = tomo.shape[0]/ni
fig, ax = plt.subplots(ni, nj, figsize=(2*nj, 2*ni))

for i in range(ni):
    for j in range(nj):
        k = i*nj + j
        ax[i,j].imshow(tomo[k], vmin=vmin, vmax=vmax)
        ax[i,j].set_title('t=%.3fs' % tomo_t[k])
        ax[i,j].set_axis_off()

plt.show()
