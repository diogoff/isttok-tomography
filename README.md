# ISTTOK Tokamak Engineering and Operation

This repository contains the source code for the tomography course at the ISTTOK training program on [Tokamak Engineering and Operation](https://isttok.tecnico.ulisboa.pt/~isttok.daemon/index.php?title=Training).

The tomography course takes place on Friday, July 26, 2019.

The code is based on a 2-camera setup available at ISTTOK described in the [MSc thesis](https://fenix.tecnico.ulisboa.pt/downloadFile/563345090414094/Dissertacao.pdf) of F. L. Burnay (in portuguese). The cameras are placed on the top and on the right-hand side of the tokamak section showed bellow. 

<img src="https://raw.githubusercontent.com/Europium-152/isttok-tomography-2019/master/images/port8.PNG" width="50%" alt="port8">

For a detailed description of tomography methods (in english) refer to the [PhD thesis](http://bibliotecas.utl.pt/cgi-bin/koha/opac-detail.pl?biblionumber=428085) of P. J. Carvalho, which also describes the previous iteration of the tomography diagnostic at ISTTOK.

For a different setup, feel free to adapt this code according to the license terms.

## Cameras

- Run `cameras.py` to find the lines of sight for each camera.

    - The two cameras are referred to as top (t) and front (f).

    - The pinhole and detector positions are provided in the code.
    
    - The vessel has a circular cross section that is assumed to be centered at (0,0) in the xy-plane.
    
    - An output file `cameras.csv` will be created with the start and end positions for each line of sight, as well as the corresponding geometric étendue. 
    
![cameras](https://raw.githubusercontent.com/Europium-152/isttok-tomography-2019/master/images/cameras.png)

## Projections

- Run `projections.py` to find the projections from pixel values to detector measurements.

    - The pixel resolution for the x- and y-axis are defined in the code.
    
    - When a line of sight crosses a pixel, the contribution of that pixel is assumed to be proportionate to the length of the intersection between the line and the pixel.
    
    - When a line of sight does not cross a pixel, the contribution of that pixel is zero, since there is no intersection.
    
    - Each line of sight is weighted according to it's étendue, which is experimentally known.

    - The projections will be saved to the output file `projections.npy`.

![projections-top](https://raw.githubusercontent.com/Europium-152/isttok-tomography-2019/master/images/projections-top.png)
![projections-front](https://raw.githubusercontent.com/Europium-152/isttok-tomography-2019/master/images/projections-front.png)

## Signals

- Run `signals.py` to get the signals from each camera, for a given shot number.

    - The code uses the SDAS API that can be downloaded and installed from [here](http://metis.ipfn.ist.utl.pt/CODAC/IPFN_Software/SDAS/Access/Python).
    
    - The shot number is indicated in the code.
    
    - The data acquisition channels that correspond to each camera detector are indicated in the code.
    
    - The signal offset is removed based on the signal average for _t_ < 0 s.
    
    - The signals are subsampled from 10 kHz to 1 kHz.
    
    - The signals are clipped to zero to remove any negative values.
    
    - The signals data and time are stored separately in `signals_data.npy` and `signals_time.npy`.
    
![signals-top](https://raw.githubusercontent.com/Europium-152/isttok-tomography-2019/master/images/signals-top.png)
![signals-front](https://raw.githubusercontent.com/Europium-152/isttok-tomography-2019/master/images/signals-front.png)

## Reconstructions

- Run `reconstructions.py` to reconstruct the plasma profile at specific time points.

    - The regularization is based on the horizontal and vertical differences between pixels.
    
    - The pixels outside the vessel have an additional regularization imposed on them.

    - The regularization weights are indicated in the code.
    
    - The time points for the reconstructions are indicated in the code.
    
![reconstructions](https://raw.githubusercontent.com/Europium-152/isttok-tomography-2019/master/images/reconstructions.png)
