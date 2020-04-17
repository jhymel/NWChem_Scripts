# Title: computeGradients.py
# Date: 4/17/2020
# This script writes grad0 by parsing lines below particular flags in the output file of a gradient calculation.
# These flags differ depending on if a Hartree-Fork or DFT level of theory is used.
# This script differs from the readForces.py file used in the analytical gradients directory since it takes in the 
# zero-point energies with each atom shifted in the +/- x,y,z directions and computes central finite differences in 
# order to create the gradients.

import os
import commands
import sys

inputGeom = sys.argv[1]
stepSize = float(sys.argv[2])

home = os.getcwd()

outputFiles = [f for f in os.listdir(os.path.join(home)) if f.endswith('.out')]
outputFiles.sort()

numberOfFiles = len(outputFiles)-1
l = range(numberOfFiles)
energies = []
atom = []
axisCount = 0
for i,j in zip(l,l[1:])[::2]:
	if 'scf' == str(commands.getoutput("tail -1 gradInput.nw" % i)).split(' ')[1].lower():
		left = float(commands.getoutput("grep 'Total SCF energy' input%i.out | tail -1 | awk '{print $5}'" % i))
		right = float(commands.getoutput("grep 'Total SCF energy' input%i.out | tail -1 | awk '{print $5}'" % j))
	elif 'dft' == str(commands.getoutput("tail -1 gradInput.nw" % i)).split(' ')[1].lower():
                left = float(commands.getoutput("grep 'Total DFT energy' input%i.out | tail -1 | awk '{print $5}'" % i))
                right = float(commands.getoutput("grep 'Total DFT energy' input%i.out | tail -1 | awk '{print $5}'" % j))
	gradient = ((left - right) / (2*stepSize)) * 0.529177249
	atom.append(gradient)
	if len(atom) == 3:
		energies.append(atom)
		atom = []
atomNames = []
tmpList = []
with open(inputGeom,'r') as f:
	for line in f:
		tmpList.append([ x for x in line.split()])
	atomNames = [x[0] for x in tmpList]
	print (atomNames)

with open('grad0','w+') as g:
	for i in energies:
		for j in i:
			g.write(str(j))
			g.write('\n')
