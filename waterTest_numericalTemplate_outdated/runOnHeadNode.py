import os
import sys

home = os.getcwd()

slurmTemplate = sys.argv[1]

inputList = [f for f in os.listdir(os.path.join(home)) if f.endswith('.nw')]
inputList.sort()
'''
print (inputList)
with open('run.slurm','w+') as g:
	with open(slurmTemplate,'r') as f:
		for line in f:
			g.write(line)
		for i in inputList:
			g.write('mpirun nwchem %s > %s.out' % (i,i[:-3]) + '\n')
'''

for i in inputList:
	os.system('mpirun -np 2 nwchem %s > %s.out' % (i,i[:-3]) + '\n')
