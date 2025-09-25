# TERRA-RGRGG-dT
This tutorial is for the simple simulation of TERRA RNA in the condensate of RGRGG+dT   
<img src="./image1.png" width="300" height="300"/>

## Dependencies
1. [PeptideBuilder](https://github.com/clauswilke/PeptideBuilder)   
2. [NAB](https://biobb-amber.readthedocs.io/en/latest/nab.html) in [biobb_amber](https://biobb-amber.readthedocs.io/en/latest/index.html)
3. Gromacs   

## Example:
TERRA RNA in RGRGG+dT5, using amber [ff14sb_OL15 force field](https://fch.upol.cz/ff_ol/gmxOL15.php)   

## Flow:   
**1. prepare RGRGG**
>a. PeptideBuilder to create the pdb file   
b. run a quick simulation of monomer in water

**2. prepare dT5**
>a. NAB to create the pdb file  
b. run a quick simulation of monomer in water

**3. prepare TERRA G4 pdb file**
>a. 