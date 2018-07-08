from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------------------------

from sdas.core.client.SDASClient import SDASClient
from sdas.core.SDAStime import TimeStamp

client = SDASClient('baco.ipfn.tecnico.ulisboa.pt', 8888)

def LoadSdasData(channelID, shotnr):
    dataStruct = client.getData(channelID, '0x0000', shotnr)
    dataArray = dataStruct[0].getData()
    len_d = len(dataArray)
    tstart = dataStruct[0].getTStart()
    tend = dataStruct[0].getTEnd()
    tbs= (tend.getTimeInMicros() - tstart.getTimeInMicros())*1.0/len_d
    events = dataStruct[0].get('events')[0]
    tevent = TimeStamp(tstamp=events.get('tstamp'))
    delay = tstart.getTimeInMicros() - tevent.getTimeInMicros()
    timeVector = np.linspace(delay,delay+tbs*(len_d-1),len_d)
    return [dataArray, timeVector]

# -------------------------------------------------------------------------

shot = 17552

channels = [
    # top camera
    'TR512_TOMOGRAPHY.TR512_B02.CHANNEL_0',
    'TR512_TOMOGRAPHY.TR512_B02.CHANNEL_1',
    'TR512_TOMOGRAPHY.TR512_B02.CHANNEL_2',
    'TR512_TOMOGRAPHY.TR512_B02.CHANNEL_3',
    'TR512_TOMOGRAPHY.TR512_B02.CHANNEL_4',
    'TR512_TOMOGRAPHY.TR512_B02.CHANNEL_5',
    'TR512_TOMOGRAPHY.TR512_B02.CHANNEL_6',
    'TR512_TOMOGRAPHY.TR512_B02.CHANNEL_7',
    # front camera
    'TR512_TOMOGRAPHY.TR512_B00.CHANNEL_0',
    'TR512_TOMOGRAPHY.TR512_B00.CHANNEL_1',
    'TR512_TOMOGRAPHY.TR512_B00.CHANNEL_2',
    'TR512_TOMOGRAPHY.TR512_B00.CHANNEL_3',
    'TR512_TOMOGRAPHY.TR512_B00.CHANNEL_4',
    'TR512_TOMOGRAPHY.TR512_B00.CHANNEL_5',
    'TR512_TOMOGRAPHY.TR512_B00.CHANNEL_6',
    'TR512_TOMOGRAPHY.TR512_B00.CHANNEL_7',
    # bottom camera
    'TR512_TOMOGRAPHY.TR512_B01.CHANNEL_0',
    'TR512_TOMOGRAPHY.TR512_B01.CHANNEL_1',
    'TR512_TOMOGRAPHY.TR512_B01.CHANNEL_2',
    'TR512_TOMOGRAPHY.TR512_B01.CHANNEL_3',
    'TR512_TOMOGRAPHY.TR512_B01.CHANNEL_4',
    'TR512_TOMOGRAPHY.TR512_B01.CHANNEL_5',
    'TR512_TOMOGRAPHY.TR512_B01.CHANNEL_6',
    'TR512_TOMOGRAPHY.TR512_B01.CHANNEL_7']

signals_data = []
signals_time = []

for channel in channels:
    print('channel:', channel)
    [data, time] = LoadSdasData(channel, shot)
    i0 = np.argmin(np.fabs(time))
    data -= np.mean(data[:i0])
    time *= 1e-6
    n = 200
    data = np.cumsum(data, axis=0)
    data = (data[n:]-data[:-n])/n
    data = data[::n]
    data = np.clip(data, 0., None)
    time = time[n//2::n]
    time = time[:data.shape[0]]
    signals_data.append(data)
    signals_time.append(time)
    plt.plot(time, data)
    if channel == channels[7]:
        plt.title('signals (top camera)')
        plt.xlabel('t (s)')
        plt.legend()
        plt.show()
    if channel == channels[15]:
        plt.title('signals (front camera)')
        plt.xlabel('t (s)')
        plt.legend()
        plt.show()
    if channel == channels[23]:
        plt.title('signals (bottom camera)')
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
