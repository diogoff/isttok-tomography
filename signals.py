from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------------------------

from sdas.core.client.SDASClient import SDASClient
from sdas.core.SDAStime import TimeStamp

client = SDASClient('baco.ipfn.tecnico.ulisboa.pt', 8888)


def get_data(shot, channel):
    info = client.getData(channel, '0x0000', shot)
    data = info[0].getData()
    t0 = TimeStamp(tstamp=info[0]['events'][0]['tstamp']).getTimeInMicros()
    t1 = info[0].getTStart().getTimeInMicros()
    t2 = info[0].getTEnd().getTimeInMicros()
    dt = float(t2-t1)/float(len(data))
    time = np.arange(t1-t0, t2-t0, dt, dtype=data.dtype)*1e-6
    return data, time


# -------------------------------------------------------------------------

shot = 47218

channels = [
    # Top camera
    'MARTE_NODE_IVO3.DataCollection.Channel_182',  # top sensor 04
    'MARTE_NODE_IVO3.DataCollection.Channel_181',  # top sensor 05
    'MARTE_NODE_IVO3.DataCollection.Channel_184',  # top sensor 06
    'MARTE_NODE_IVO3.DataCollection.Channel_179',  # top sensor 07
    'MARTE_NODE_IVO3.DataCollection.Channel_178',  # top sensor 08
    'MARTE_NODE_IVO3.DataCollection.Channel_185',  # top sensor 09
    'MARTE_NODE_IVO3.DataCollection.Channel_183',  # top sensor 10
    'MARTE_NODE_IVO3.DataCollection.Channel_180',  # top sensor 11
    'MARTE_NODE_IVO3.DataCollection.Channel_004',  # top sensor 12
    'MARTE_NODE_IVO3.DataCollection.Channel_005',  # top sensor 13
    'MARTE_NODE_IVO3.DataCollection.Channel_003',  # top sensor 14
    'MARTE_NODE_IVO3.DataCollection.Channel_007',  # top sensor 15
    'MARTE_NODE_IVO3.DataCollection.Channel_000',  # top sensor 16
    'MARTE_NODE_IVO3.DataCollection.Channel_001',  # top sensor 17
    'MARTE_NODE_IVO3.DataCollection.Channel_002',  # top sensor 18
    'MARTE_NODE_IVO3.DataCollection.Channel_006',  # top sensor 19
    # Front camera
    'MARTE_NODE_IVO3.DataCollection.Channel_190',  # front sensor 04
    'MARTE_NODE_IVO3.DataCollection.Channel_189',  # front sensor 05
    'MARTE_NODE_IVO3.DataCollection.Channel_192',  # front sensor 06
    'MARTE_NODE_IVO3.DataCollection.Channel_187',  # front sensor 07
    'MARTE_NODE_IVO3.DataCollection.Channel_186',  # front sensor 08
    'MARTE_NODE_IVO3.DataCollection.Channel_193',  # front sensor 09
    'MARTE_NODE_IVO3.DataCollection.Channel_191',  # front sensor 10
    'MARTE_NODE_IVO3.DataCollection.Channel_188',  # front sensor 11
    'MARTE_NODE_IVO3.DataCollection.Channel_012',  # front sensor 12
    'MARTE_NODE_IVO3.DataCollection.Channel_013',  # front sensor 13
    'MARTE_NODE_IVO3.DataCollection.Channel_011',  # front sensor 14
    'MARTE_NODE_IVO3.DataCollection.Channel_015',  # front sensor 15
    'MARTE_NODE_IVO3.DataCollection.Channel_008',  # front sensor 16
    'MARTE_NODE_IVO3.DataCollection.Channel_009',  # front sensor 17
    'MARTE_NODE_IVO3.DataCollection.Channel_010',  # front sensor 18
    'MARTE_NODE_IVO3.DataCollection.Channel_014',  # front sensor 19
    # Bottom camera
    # 'MARTE_NODE_IVO3.DataCollection.Channel_198',  # bottom sensor 04   ***UNCOMMENT TO ADD BOTTOM CAMERA***
    # 'MARTE_NODE_IVO3.DataCollection.Channel_197',  # bottom sensor 05
    # 'MARTE_NODE_IVO3.DataCollection.Channel_200',  # bottom sensor 06
    # 'MARTE_NODE_IVO3.DataCollection.Channel_195',  # bottom sensor 07
    # 'MARTE_NODE_IVO3.DataCollection.Channel_194',  # bottom sensor 08
    # 'MARTE_NODE_IVO3.DataCollection.Channel_201',  # bottom sensor 09
    # 'MARTE_NODE_IVO3.DataCollection.Channel_199',  # bottom sensor 10
    # 'MARTE_NODE_IVO3.DataCollection.Channel_196',  # bottom sensor 11
    # 'MARTE_NODE_IVO3.DataCollection.Channel_020',  # bottom sensor 12
    # 'MARTE_NODE_IVO3.DataCollection.Channel_021',  # bottom sensor 13
    # 'MARTE_NODE_IVO3.DataCollection.Channel_019',  # bottom sensor 14
    # 'MARTE_NODE_IVO3.DataCollection.Channel_023',  # bottom sensor 15
    # 'MARTE_NODE_IVO3.DataCollection.Channel_016',  # bottom sensor 16
    # 'MARTE_NODE_IVO3.DataCollection.Channel_017',  # bottom sensor 17
    # 'MARTE_NODE_IVO3.DataCollection.Channel_018',  # bottom sensor 18
    # 'MARTE_NODE_IVO3.DataCollection.Channel_022',  # bottom sensor 19
]

signals_data = []
signals_time = []

for channel in channels:
    print('channel:', channel)
    data, time = get_data(shot, channel)
    i0 = np.argmin(np.fabs(time))
    data -= np.mean(data[:i0])
    n = 10
    data = np.cumsum(data, axis=0)
    data = (data[n:]-data[:-n])/n
    data = data[::n]
    data = np.clip(data, 0., None)
    time = time[n//2::n]
    time = time[:data.shape[0]]
    signals_data.append(data)
    signals_time.append(time)
    plt.plot(time, data)
    if channel == channels[15]:
        plt.title('signals (top camera)')
        plt.xlabel('t (s)')
        plt.legend()
        plt.figure()
    if channel == channels[31]:
        plt.title('signals (front camera)')
        plt.xlabel('t (s)')
        plt.legend()
        # plt.figure()                            ***UNCOMMENT TO ADD BOTTOM CAMERA***
    # if channel == channels[47]:
    #     plt.title('signals (bottom camera)')
    #     plt.xlabel('t (s)')
    #     plt.legend()

plt.show()

# -------------------------------------------------------------------------

signals_data = np.array(signals_data)
signals_time = np.array(signals_time)

print('signals_data:', signals_data.shape, signals_data.dtype)
print('signals_time:', signals_time.shape, signals_time.dtype)

# -------------------------------------------------------------------------

fname = 'signals_data.npy'
print('Writing:', fname)
np.save(fname, signals_data)

fname = 'signals_time.npy'
print('Writing:', fname)
np.save(fname, signals_time)
