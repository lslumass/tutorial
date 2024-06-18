This turotial is for the protein-bilayer binding system, where protein was firstly located in water, far away from bilayer.

## Dependencies:   
1. [CHARMM-GUI](https://www.charmm-gui.org/)   
2. Gromacs   

## Example:
KR8 + POPC/POPG bilayer, using Charmm36 FF.   

## Flow:
1. prepare charmm36 ff file for gromacs, download from [MacKerell Lab](https://mackerell.umaryland.edu/charmm_ff.html), extract the file to where you are gona run gmx. The pbd2gmx can automatically detect these files.      
2. prepare the pdb file of protein, and then the itp file:   
```
gmx pdb2gmx -f kr8_at.pdb -o kr8.gro -ignh -ter -water tip3p -p kr8.top   
```
select the terminals, then modify the obtained kr8.top, delete the "#include", "[ system ]", and "[ molecules ]" sections, which will be included in topol.top file. Then save as kr8.itp. (posre.itp should be included if nessecary)   
3. prepare the hydrated bilayer with ions using Charmm-GUI   
