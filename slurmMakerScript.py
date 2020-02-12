import os

home = os.getcwd()

inputList = [f for f in os.listdir(os.path.join(home)) if f.endswith('.nw')]


print (inputList)

for i in inputList:
	with open(i[:-3] + '.slurm', 'w+') as g:
		with open('blankSlurm','r') as f:
			for line in f:
				g.write(line)
			g.write('mpirun nwchem %s > %s.out' % (i,i[:-3]))
