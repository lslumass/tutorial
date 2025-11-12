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
missed_loop1 = ["1-13", "95-140"]
missed_loop2 = ["1-20", "100-140"]
out = 'alignment.ali'       

# expand the missing residues
res_missed1 = []
for sec in missed_loop1:
    i, j = map(int, sec.split('-'))
    for res in range(i, j+1):
        res_missed1.append(res)

res_missed2 = []
for sec in missed_loop2:
    i, j = map(int, sec.split('-'))
    for res in range(i, j+1):
        res_missed2.append(res)

# create alignment.ali file
print('create ali file\n')
with open(out, 'w') as f:
    print('>P1;miss\nstructureX:40mer::A::::::', file=f)
    tem1 = ''
    tem2 = ''
    for n in range(num):
        if n % 2 == 0:
            res_missed = res_missed1
        else:
            res_missed = res_missed2
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
