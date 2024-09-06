import MDAnalysis as mda
import numpy as np

u = mda.Universe('md.tpr', 'md.xtc')
num_lipid = 675
with open('area_per_lipid.dat', 'w') as f:
    for ts in u.trajectory:
        lx = ts.dimensions[0]/10.0
        ly = ts.dimensions[1]/10.0
        area = lx*ly/num_lipid
        print(ts.time, area, file=f)
#    print(ts.dimensions[0])