# ISTTOK Tokamak Engineering and Operation

This repository contains the source code for the tomography session at the ISTTOK training program on [Tokamak Engineering and Operation](https://isttok.tecnico.ulisboa.pt/~isttok.daemon/index.php?title=Training).

The tomography session takes place on Friday, July 26, 2019 at 9:00 in room C13.

The code is based on a two-camera setup described in the [MSc thesis](https://fenix.tecnico.ulisboa.pt/downloadFile/563345090414094/Dissertacao.pdf) of F. L. Burnay (in Portuguese). The vertical camera is on the top and the horizontal camera is on the low-field side of the vessel, as shown in the figure below. (A third camera placed at the bottom is currently not operational.)

<p align="center"><img src="https://raw.githubusercontent.com/diogoff/isttok-tomography/master/images/ports.png" width="50%"></p>

A more detailed discussion of tomography methods can be found in the [PhD thesis](http://bibliotecas.utl.pt/cgi-bin/koha/opac-detail.pl?biblionumber=428085) of P. J. Carvalho, which also describes the previous setup of the tomography diagnostic at ISTTOK.

For different setups, feel free to adapt this code according to the license terms.

## Cameras

- Run `cameras.py` to find the lines of sight for each camera.

    - The two cameras are referred to as vertical (v) and horizontal (h).

    - The pinhole and detector positions are provided in the code, together with étendue values obtained by calibration.
    
    - The vessel has a circular cross section that is assumed to be centered at (0,0) in the xy-plane.
    
    - An output file `cameras.csv` will be created with the start and end positions for each line of sight, together with the corresponding étendue. 
    
<p align="center"><img src="https://raw.githubusercontent.com/diogoff/isttok-tomography/master/images/cameras.png" width="50%"></p>

## Projections

- Run `projections.py` to find the projections from pixel values to detector measurements.

    - The pixel resolution for the x- and y-axis are defined in the code.
    
    - When a line of sight crosses a pixel, the contribution of that pixel is assumed to be proportionate to the length of the intersection between the line and the pixel.
    
    - When a line of sight does not cross a pixel, the contribution of that pixel is zero, since there is no intersection.
    
    - Each line of sight is weighted according to the corresponding étendue, which was obtained experimentally.

    - The projections will be saved to the output file `projections.npy`.

<p align="center"><img src="https://raw.githubusercontent.com/diogoff/isttok-tomography/master/images/projections-vertical.png" width="50%"></p>
<p align="center"><img src="https://raw.githubusercontent.com/diogoff/isttok-tomography/master/images/projections-horizontal.png" width="50%"></p>

## Signals

- Run `signals.py` to get the signals from each camera, for a given shot number.

    - The code uses the SDAS API that can be downloaded and installed from [here](http://metis.ipfn.ist.utl.pt/CODAC/IPFN_Software/SDAS/Access/Python).
    
    - The shot number is indicated in the code. (The present setup is valid from shot number 47216 to 47262.)
    
    - The data acquisition channels that correspond to each camera detector are indicated in the code.
    
    - The signal offset is removed based on the signal average for _t_ < 0 s.
    
    - The signals are subsampled from 10 kHz to 1 kHz.
    
    - The signals are clipped to zero to remove any negative values.
    
    - The signals data and time are stored separately in `signals_data.npy` and `signals_time.npy`.
    
<p align="center"><img src="https://raw.githubusercontent.com/diogoff/isttok-tomography/master/images/signals-vertical.png" width="50%"></p>
<p align="center"><img src="https://raw.githubusercontent.com/diogoff/isttok-tomography/master/images/signals-horizontal.png" width="50%"></p>

## Reconstructions

- Run `reconstructions.py` to reconstruct the plasma profile at specific points in time.

    - The regularization is based on the differences between adjacent pixels.
    
    - The pixels outside the vessel have an additional regularization imposed on them.

    - The regularization weights are indicated in the code.
    
    - The time points for the reconstructions are indicated in the code.
    
<p align="center"><img src="https://raw.githubusercontent.com/diogoff/isttok-tomography/master/images/reconstructions.png" width="50%"></p>
