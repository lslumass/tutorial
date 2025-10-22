import MDAnalysis as mda
from MDAnalysis.analysis import align
import sys


ref = sys.argv[1]
mob = sys.argv[2]

u1 = mda.Universe(ref)
u2 = mda.Universe(mob) 
align.alignto(u2, u1, select='backbone and resid 37:97', weights='mass')

core1 = u1.select_atoms('resid 37:97')
core2 = u2.select_atoms('resid 37:97')

core2.positions = core1.positions

u2.atoms.write(f'{mob[:-4]}_replaced.pdb')