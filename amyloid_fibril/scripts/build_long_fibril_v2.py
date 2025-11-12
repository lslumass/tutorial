#!/usr/bin/python
from __future__ import division
import sys
import argparse
import numpy as np
from pathlib import Path
import MDAnalysis as mda
from MDAnalysis.analysis import align
from MDAnalysis.coordinates import PDB

'''
This script is for build longer fibril of a-synu from PDB # 6OSJ
Author: Shanlong Li
Date: Oct-21-2024
'''

## input information
parser = argparse.ArgumentParser(
  prog='FibrilBuilder',
  description='Build longer Fibril.'
)
parser.add_argument('-i', '--inp', help='input pdb file')
parser.add_argument('-o', '--out', help='output pbd file')
parser.add_argument('-n', '--num', type=int, help='number of layers, each layer has two monomers')
args = parser.parse_args()

inp = args.inp
out = args.out
num = args.num

## main
u = mda.Universe(inp)

sel = u.select_atoms("chainID G H I J")
ref = u.select_atoms("chainID G H")
mobile = sel.copy()

with mda.Writer(out, multiframe=False, reindex=False) as f:
    f.write(u.select_atoms("all"))
    for i in range(num-5):
        align.alignto(mobile, ref, select=("chainID I J", "chainID G H"))
        f.write(mobile.select_atoms("chainID G H"))
        ref = mobile.copy()
print('Done!')
