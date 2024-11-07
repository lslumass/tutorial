from sys import argv
from modeller import *
from modeller.automodel import *
from modeller.parallel import *
#from mymodel import MyModel

# monomer sequence file
with open(argv[1], 'r') as f:
    seq = f.readlines()[1][:-1]

# number of monomers
num = int(argv[2])
# missed residues
missed_loop = ["1-36", "98-140"]
out = 'alignment.ali'       

# expand the missing residues
res_missed = []
for sec in missed_loop:
    i, j = map(int, sec.split('-'))
    for res in range(i, j+1):
        res_missed.append(res)

# create alignment.ali file
print('create ali file\n')
with open(out, 'w') as f:
    print('>P1;miss\nstructureX:40mer::A::::::', file=f)
    tem1 = ''
    tem2 = ''
    for n in range(num):
        seq_miss = ''.join('-' if i+1 in res_missed else char for i, char in enumerate(seq))
        seq_fill = ''.join(char for char in seq)
        if n != num-1:
            tem1 += seq_miss + '/\n'
            tem2 += seq_fill + '/\n'
        else:
            tem1 += seq_miss + '*'
            tem2 += seq_fill + '*'
    print(tem1, file=f)
    print("\n>P1;fill\nsequence:::::::::", file=f)
    print(tem2, file=f)

print('fill the missing residues\n')
env = Environ()
env.io.atom_files_directory = ['.', './atom_files']

segments, residues = [], []
for i in range(num):
    segments.append('X')
    residues.append(1)
class MyModel(LoopModel):
    def special_patches(self, aln):
        self.rename_segments(segment_ids=segments, renumber_residues=residues)
a = MyModel(env, alnfile='alignment.ali', knowns='miss', sequence='fill')
a.starting_model = 1
a.ending_model = 1
a.loop.starting_model = 1
a.loop.ending_model = 1
a.loop.md_level = refine.very_fast
a.make()

print('Finished!')
