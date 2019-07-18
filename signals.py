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

shot = 47238

channels = [

    # vertical camera
    'MARTE_NODE_IVO3.DataCollection.Channel_182',  # vertical sensor 04
    'MARTE_NODE_IVO3.DataCollection.Channel_181',  # vertical sensor 05
    'MARTE_NODE_IVO3.DataCollection.Channel_184',  # vertical sensor 06
    'MARTE_NODE_IVO3.DataCollection.Channel_179',  # vertical sensor 07
    'MARTE_NODE_IVO3.DataCollection.Channel_178',  # vertical sensor 08
    'MARTE_NODE_IVO3.DataCollection.Channel_185',  # vertical sensor 09
    'MARTE_NODE_IVO3.DataCollection.Channel_183',  # vertical sensor 10
    'MARTE_NODE_IVO3.DataCollection.Channel_180',  # vertical sensor 11
    'MARTE_NODE_IVO3.DataCollection.Channel_004',  # vertical sensor 12
    'MARTE_NODE_IVO3.DataCollection.Channel_005',  # vertical sensor 13
    'MARTE_NODE_IVO3.DataCollection.Channel_003',  # vertical sensor 14
    'MARTE_NODE_IVO3.DataCollection.Channel_007',  # vertical sensor 15
    'MARTE_NODE_IVO3.DataCollection.Channel_000',  # vertical sensor 16
    'MARTE_NODE_IVO3.DataCollection.Channel_001',  # vertical sensor 17
    'MARTE_NODE_IVO3.DataCollection.Channel_002',  # vertical sensor 18
    'MARTE_NODE_IVO3.DataCollection.Channel_006',  # vertical sensor 19

    # horizontal camera
    'MARTE_NODE_IVO3.DataCollection.Channel_190',  # horizontal sensor 04
    'MARTE_NODE_IVO3.DataCollection.Channel_189',  # horizontal sensor 05
    'MARTE_NODE_IVO3.DataCollection.Channel_192',  # horizontal sensor 06
    'MARTE_NODE_IVO3.DataCollection.Channel_187',  # horizontal sensor 07
    'MARTE_NODE_IVO3.DataCollection.Channel_186',  # horizontal sensor 08
    'MARTE_NODE_IVO3.DataCollection.Channel_193',  # horizontal sensor 09
    'MARTE_NODE_IVO3.DataCollection.Channel_191',  # horizontal sensor 10
    'MARTE_NODE_IVO3.DataCollection.Channel_188',  # horizontal sensor 11
    'MARTE_NODE_IVO3.DataCollection.Channel_012',  # horizontal sensor 12
    'MARTE_NODE_IVO3.DataCollection.Channel_013',  # horizontal sensor 13
    'MARTE_NODE_IVO3.DataCollection.Channel_011',  # horizontal sensor 14
    'MARTE_NODE_IVO3.DataCollection.Channel_015',  # horizontal sensor 15
    'MARTE_NODE_IVO3.DataCollection.Channel_008',  # horizontal sensor 16
    'MARTE_NODE_IVO3.DataCollection.Channel_009',  # horizontal sensor 17
    'MARTE_NODE_IVO3.DataCollection.Channel_010',  # horizontal sensor 18
    'MARTE_NODE_IVO3.DataCollection.Channel_014',  # horizontal sensor 19

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
        plt.title('signals (vertical camera)')
        plt.xlabel('t (s)')
        plt.legend()
        plt.show()
    if channel == channels[31]:
        plt.title('signals (horizontal camera)')
        plt.xlabel('t (s)')
        plt.legend()
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
