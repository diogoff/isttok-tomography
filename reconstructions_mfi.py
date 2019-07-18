from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
from skimage.draw import ellipse


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

# Reconstruction Size and Resolution -----------------------------------------------


n_rows = projections.shape[1]
n_cols = projections.shape[2]

res_x = 200 / float(n_cols)
res_y = 200 / float(n_rows)  # x,y (mm)

# x and y arrays for plotting purposes. Coordinates represent the top left corner of each pixel
x_array_plot = (np.arange(n_cols + 1) - n_cols / 2.) * res_x
y_array_plot = (n_rows / 2. - np.arange(n_rows + 1)) * res_y

# x and y arrays for calculation purposes. Coordinates represent the center of each pixel
x_array = np.arange(n_cols) * res_x - n_cols / 2. * res_x
y_array = n_rows / 2. * res_y - np.arange(n_rows) * res_y

# Masks, negative mask: zeros inside, positive mask: zeros outside -------------------------------

mask_radius = 85.  # Outside this radius the plasma is expected to have zero emissivity

ii, jj = ellipse(n_rows / 2., n_cols / 2., mask_radius / res_y, mask_radius / res_x)
mask_negative = np.ones((n_rows, n_cols))
mask_negative[ii, jj] = 0.
mask_positive = np.zeros((n_rows, n_cols))
mask_positive[ii, jj] = 1.


# -------------------------------------------------------------------------

projections = projections * mask_positive

P = projections.reshape((projections.shape[0], -1))

print('P:', P.shape, P.dtype)

# -------------------------------------------------------------------------

Dh = np.eye(n_rows*n_cols) - np.roll(np.eye(n_rows*n_cols), 1, axis=1)
Dv = np.eye(n_rows*n_cols) - np.roll(np.eye(n_rows*n_cols), n_cols, axis=1)

print('Dh:', Dh.shape, Dh.dtype)
print('Dv:', Dv.shape, Dv.dtype)

# -------------------------------------------------------------------------

Io = np.eye(n_rows*n_cols) * mask_negative.flatten()

print('Io:', Io.shape, Io.dtype)

# -------------------------------------------------------------------------

Pt = np.transpose(P)
PtP = np.dot(Pt, P)

ItIo = np.dot(np.transpose(Io), Io)

alpha_1 = 50.
alpha_2 = alpha_1
alpha_3 = alpha_1*10000

# -------------------------------------------------------------------------

tomo = []
tomo_t = np.arange(0.310, 0.331, 0.001)

mfi_max_iterations = 10     # Maximum number of iterations before MFI quits
stop_criteria = 0.01        # Break when percentage difference between iterations reaches this value (between 0 & 1)

for t in tomo_t:

    # Get the signals for the desired time instant ------------------------
    time_index = np.argmin(np.fabs(signals_time[0] - t))
    # f = signals_data[:, time_index].reshape((-1, 1))
    f = signals_data[:, time_index]

    # f[:16] = f[:16] * 3 * np.sum(f[16:]) / np.sum(f[:16])

    # The zeroth iteration of g is an array of ones  ----------------------
    g_previous = np.ones(n_rows * n_cols)

    for i in range(mfi_max_iterations):

        # Weight matrix ------------------------------------------------------------
        W = np.diag(1.0 / g_previous)

        # Weighted derivatives -----------------------------------------------------
        DtWDh = np.dot(np.transpose(Dh), np.dot(W, Dh))
        DtWDv = np.dot(np.transpose(Dv), np.dot(W, Dv))

        inv = np.linalg.inv(alpha_1 * DtWDh + alpha_2 * DtWDv + PtP + alpha_3 * ItIo)

        M = np.dot(inv, Pt)

        g = np.dot(M, f)

        # Clip to small number to prevent infinities on weight matrix --------------
        np.clip(g, a_min=1e-20, a_max=None, out=g)

        cov = 1. - np.corrcoef(g, g_previous)

        error = cov[0, 1]

        print("Iteration %d changed by %.4f%%" % (i + 1, error * 100.))

        if error < stop_criteria:  # Check if convergence was achieved
            print("Minimum Fisher converged after %d iterations." % (i + 1))
            tomo.append(g.reshape((n_rows, n_cols)))
            break

        elif (i + 1) == mfi_max_iterations:  # If maximum iterations has been reached break just before the `for loop` does
            print("WARNING: Minimum Fisher did not converge after %d iterations." % (i + 1))
            tomo.append(g.reshape((n_rows, n_cols)))
            break

        else:
            g_previous = np.array(g)  # Copy values. Otherwise g and g_previous become pointers to the same address


tomo = np.array(tomo)

print('tomo:', tomo.shape, tomo.dtype)
print('tomo_t:', tomo_t.shape, tomo_t.dtype)

# -------------------------------------------------------------------------

vmin = 0.
vmax = np.max(tomo)

ni = 4
nj = tomo.shape[0]//ni
fig, ax = plt.subplots(ni, nj, figsize=(2*nj, 2*ni))

for i in range(ni):
    for j in range(nj):
        k = i*nj + j
        ax[i,j].imshow(tomo[k], vmin=vmin, vmax=vmax)
        ax[i,j].set_title('t=%.3fs' % tomo_t[k])
        ax[i,j].set_axis_off()

plt.show()
