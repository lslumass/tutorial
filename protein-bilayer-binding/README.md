This turotial is for the multiple-protein_-_bilayer binding system, where multiple copies of proteins were firstly distributed in water, far away from bilayer.

## Dependencies:   
1. [CHARMM-GUI](https://www.charmm-gui.org/)   
2. Gromacs   
3. [packmol](https://m3g.github.io/packmol/)   

## Example:
KR8 + POPC/POPG bilayer, using Charmm36 FF.   

## Flow:
**1. prepare charmm36 ff file for gromacs**:   
    download from [MacKerell Lab](https://mackerell.umaryland.edu/charmm_ff.html), extract the file to where you are gona run gmx. The pbd2gmx can automatically detect these files.      

**2. prepare the pdb file of protein, and then the itp file**:   
```
gmx pdb2gmx -f kr8_at.pdb -o kr8.gro -ignh -ter -water tip3p -p kr8.top   
```
select the terminals, then modify the obtained [kr8.top](./examples/kr8.top), delete the "#include", "[ system ]", and "[ molecules ]" sections, which will be included in topol.top file. Then save as [kr8.itp](./examples/kr8.itp). (posre.itp should be included if necessary)  

**3. run quick equilibirum simulation for KR8**   
```
a. gmx editconf -f kr8.gro -d 1.0 -bt cubic -o box.gro   
b. gmx solvate -cp box.gro -cs spc216.gro -p topol.top -o boxw.gro    
c. gmx grompp -f em.mdp -c boxw.gro -o ion.tpr -p topol.top   
d. gmx genions -s ion.tpr -o boxwion.gro -pname NA -nname CL -conc 0.035 -neutral -p topolt.top   
e. gmx grompp -f em.mdp -c boxwion.gro -p topol.top -o em.gro   
f. gmx mdrun -deffnm em -v   
g. gmx grompp -f md.mdp -c em.grp -p topol.top -o md.mdp    
h. gmx mdrun -deffnm md -v    
```
then get the equilibrated KR8 peptide, [kr8_md.gro](./examples/kr8_md.gro)   

**4. prepare the dry bilayer using Charmm-GUI.**   
build the bilayer, choose the forcefield as Charmm36    
dowload the tgz file and use the files in gromacs. convert [bilayer.gro](./examples/bilayer.gro) to [bilayer.pdb](./examples/bilayer.pdb), and also update the lipid in topol.top   
Also, you can get the itp files for lipids ([POPC.itp](./examples/POPC.itp), [POPG.itp](./examples/POPG.itp)), copy them to your folder   

**5. pack the bilayer with 10 KR8 peptides**   
```
tolerance 10.0
filetype pdb
output conf.pdb
add_box_sides 0.0

structure bilayer.pdb
  number 1
  center
  fixed 57.5 57.5 40. 0.0 0.0 0.0
end structure

structure kr8_md.pdb
  number 10
  inside box 0. 0. 0. 115. 115. 120.
end structure
```
where bilayer was placed at the bottom of the box, and KR8 were distribution within the water.   

**6. solvate the dry bilayer and peptide**   
```
gmx solvate -cp conf.pdb -cs spc216.gro -p topol.top -o conf_w.gro
```
After solvating, visualize the structure and you will see many water molecules within the hydrophobic core of the bilayer. Use remove_water_within_bilayer.pl to delete these water molecules:   
```
perl remove_water_within_bilayer.pl -in conf_w.gro -out conf_w_fix.gro -ref O13 -middle C316 -nwater 3
```
>The file names passed to -in and -out are the input and output file names, respectively. The -ref flag allows the user to set which atom is set as a "reference" to define the upper and lower boundaries of the membrane. It is wise to set this atom name to one of the atoms in the ester region of the phospholipid rather than a headgroup atom, to prevent excessive dehydration. The -middle flag specifies an atom that is representative of the middle of the bilayer (along the membrane normal, typically the z-axis) so the reference atoms can be divided into upper and lower leaflets, thus establishing the range of z-coordinate values within which water molecules will be deleted. The value passed to -nwater defines how many atoms constitute a water molecule. For SPC, there are only three atoms (OW, HW1, and HW2).

>The script tells you how many water molecules it deleted and how many water molecules remain in the system. Update the SOL line in topol.top with this updated number of water molecules.

**7. add ions**   
```
a. gmx grompp -f em.mdp -c conf_w_fix.gro -p topol.top -o ions.tpr -maxwarn 1
b. gmx genion -s ions.tpr -o conf_w_ions.gro -p topol.top -pname NA -nname CL -neutral -conc 0.035
```

**8. run simulation**   
```
a. gmx grompp -f em.mdp -c conf_w_ions.gro -p topol.top -o em
b. gmx mdrun -deffnm em -v
c. gmx grompp -f md.mdp -c em.gro -p topol.top -o md
d. gmx mdrun -deffnm md -v
```