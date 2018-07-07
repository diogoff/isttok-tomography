# ISTTOK Tokamak Engineering and Operation

This repository contains the source code for the tomography course at the ISTTOK training program on [Tokamak Engineering and Operation](https://isttok.tecnico.ulisboa.pt/~isttok.daemon/index.php?title=Training).

The code is based on the 3-camera setup described in the [PhD thesis](http://bibliotecas.utl.pt/cgi-bin/koha/opac-detail.pl?biblionumber=428085) of P. J. Carvalho.

![fig3.2](https://raw.githubusercontent.com/diogoff/isttok-tomography/master/images/fig3.2.png)

For a different setup, feel free to adapt this code according to the license terms.

## Instructions

- Run `cameras.py` to find the lines of sight for each camera.

    - The three cameras are referred to as top (t), front (f) and bottom (b).

    - The pinhole and detector positions are provided in the code.
    
    - The vessel has a circular cross section that is assumed to be centered at (0,0) in the xy-plane.
    
    - An output file `cameras.csv` will be created with the start and end positions for each line of sight.
    
![cameras](https://raw.githubusercontent.com/diogoff/isttok-tomography/master/images/cameras.png)

- Run `projections.py` to find the projections from pixel values to detector measurements.

    - The pixel resolution for the x- and y-axis are defined in the code.
    
    - When a line of sight crosses a pixel, the contribution of that pixel is assumed to be proportionate to the length of the intersection between the line and the pixel.
    
    - When a line of sight does not cross a pixel, the contribution of that pixel is zero, since there is no intersection.

    - The projections will be saved to the output file `projections.npy`.

![projmat-top](https://raw.githubusercontent.com/diogoff/isttok-tomography/master/images/projmat-top.png)
![projmat-front](https://raw.githubusercontent.com/diogoff/isttok-tomography/master/images/projmat-front.png)
![projmat-bottom](https://raw.githubusercontent.com/diogoff/isttok-tomography/master/images/projmat-bottom.png)
