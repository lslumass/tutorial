#!/usr/bin/python

'''
script for statistics of aggregation number based on Hierarchical Clustering
version 2: based on the segment
author: Shanlong Li@UMass
date: 09-01-2024
'''

from __future__ import division
import numpy as np
from multiprocessing import Pool
import MDAnalysis as mda
from MDAnalysis.analysis import distances
from functools import partial

##define calculate function
def aggr_cal(frame_index, segs, grps):
    grp_num = len(grps)
    for i in range(nmol-1):
        seg_i = segs[i]
        seg_i.universe.trajectory[frame_index]
        grp_i = grps[i]
        for j in range(i+1, nmol):
            seg_j = segs[j]
            seg_j.universe.trajectory[frame_index]
            grp_j = grps[j]
            d_arr = distances.distance_array(seg_i.positions, seg_j.positions, box=box)
            d = np.min(d_arr)
            if d <= r_criterion and grp_i != grp_j:
                grps = np.where(grps == grp_j, grp_i, grps)
                grp_num -= 1
    
    # aggr={'grp_id': number of chains in this group}
    aggr = {}
    for grp in grps:
        aggr[grp] = aggr.get(grp,0) + 1
    
    # get the number of monomers
    monomer = 0
    clusters = []
    for value in aggr.values():
        clusters.append(value)
        if value == 1:
            monomer += 1

    return monomer, len(clusters)-monomer


#some parameters which should be changed for different sys.
r_criterion = 15.0
nmol = 200
freq = 100
time_step = 0.04        # 5000*0.008=0.04 ns

u = mda.Universe('conf.psf', 'system.dcd')
box = u.dimensions
segs = []
grps = []
for i in range(200):
    seg = u.select_atoms('segid R'+str(i)+' and name P')
    segs.append(seg)
    grps.append(i)
grps = np.array(grps)

# multiprocess to calculate aggr_number for each frame
cal_per_frame = partial(aggr_cal, segs=segs, grps=grps)
frame_values = np.concatenate((np.array([0]), np.arange(freq-1, u.trajectory.n_frames, freq)))
print(frame_values)
#frame_values = np.array([-1])
n_jobs = 20

print("assign job to Pool")
with Pool(n_jobs) as worker_pool:
    result = worker_pool.map(cal_per_frame, frame_values)

## print out to the 'aggr.dat' in the order of time, monomer, aggregation number
print("write into dat file:")
with open('aggr.dat', 'w') as fout:
    for idx, frame in enumerate(frame_values):
        print((frame+1)*time_step, result[idx][0], result[idx][1], file=fout)

print("DONE!!")
