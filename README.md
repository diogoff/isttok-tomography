# ISTTOK Tokamak Engineering and Operation

This repository contains the source code for the tomography course at the ISTTOK training program on [Tokamak Engineering and Operation](https://isttok.tecnico.ulisboa.pt/~isttok.daemon/index.php?title=Training).

The code is based on the 3-camera setup described in the [PhD thesis](http://bibliotecas.utl.pt/cgi-bin/koha/opac-detail.pl?biblionumber=428085) of P. J. Carvalho.

![Cameras](https://raw.githubusercontent.com/diogoff/isttok-tomography/master/images/fig3.2.png)

For a different setup, feel free to adapt this code according to the license terms.

## Instructions

- Run `cameras.py` to find the lines of sight for each camera.

    - The three cameras are referred to as top (t), front (f) and bottom (b).

    - The pinhole and detector positions are provided in the code.
    
    - The vessel has a circular cross section that is assumed to be centered at (0,0) in the xy-plane.
    
    - An output file `cameras.csv` will be created with the start and end positions for each line of sight.
    
    - For testing, the script will read the output file and plot the lines of sight.
