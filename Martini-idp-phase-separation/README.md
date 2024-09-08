# Martini-IDP phase separation with PP scaling   

## Flow:   
0. rescale [martini_v3.0.0.itp](./martini_v300/martini_v3.0.0.itp) using [scale.py](./scripts/scale.py)   
    the bead for proteins will be added the suffix _PRO
1. build all-atom structure of IDP using [build.py](./scripts/build.py)   
2. martinize:
```martinize2 -f A1_at.pdb -o A1_topol.top -x A1_CG.pdb -ff martini3001 -ff-dir ../martini_v300_modified_protein_ff -cys auto -nt -scfix```   
3. rename the bead type in protein itp file using [rename_itp.py](./scripts/rename_itp.py)    
4. monomer simulation using original version to get collapse conformation. 