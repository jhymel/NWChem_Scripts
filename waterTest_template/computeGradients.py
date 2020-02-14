import os
import commands
import sys

stepSize = sys.argv[1]

home = os.getcwd()

outputFiles = [f for f in os.listdir(os.path.join(home)) if f.endswith('.out')]
outputFiles.sort()

numberOfFiles = len(outputFiles)-1
l = range(numberOfFiles)
energies = []
atom = []
axisCount = 0
for i,j in zip(l,l[1:])[::2]:
	#print ('input%i.out , input%i.out' %(i,j) )
	left = float(commands.getoutput("grep 'Total SCF energy' input%i.out | tail -1 | awk '{print $5}'" % i))
	right = float(commands.getoutput("grep 'Total SCF energy' input%i.out | tail -1 | awk '{print $5}'" % j))
	gradient = ((left - right) / (2*stepSize)) * 0.529177249
	atom.append(gradient)
	if len(atom) == 3:
		energies.append(atom)
		atom = []

print (energies)
