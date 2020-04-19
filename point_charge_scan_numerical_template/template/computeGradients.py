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
import numpy as np

inputGeom = sys.argv[1]
stepSize=float(commands.getoutput("sed '3q;d' gradient_estimation.out | awk '{ print $10 }'"))

home = os.getcwd()

outputFiles = [f for f in os.listdir(os.path.join(home)) if f.endswith('.out') and f.startswith('input')]
outputFiles.sort()

l = range(len(outputFiles))
energies = []
atom = []
axisCount = 0

# This complicated looking zip list is basically grabbing each pair of .out files so that those shifted in opposite (+/-) directions are together,
# this is necessary to compute the central finite difference. Example (1,2),(3,4),(5,6)...(i,j)
for i,j in zip(l,l[1:])[::2]:
	# Determine the correct grep call to make in order to retrieve energies from .out files.
	# The .lower() command makes it so that differences in case (SCF vs scf vs sCf) in the run file aren't an issue.
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

# Write grad0, the file containing forces that will be read using the read_force flag in the modified NWChem code.
with open('grad0','w+') as g:
	for i in energies:
		for j in i:
			g.write(str(j))
			g.write('\n')

# Write a human-readable form of grad0
hrg = []
labels = ['Atoms','Force(X)','Force(Y)','Force(Z)']
hrg.append(labels)
for lineNumber, line in enumerate(energies):
	line.insert(0,atomNames[lineNumber])
	hrg.append(line)
np.vstack(hrg)
np.savetxt('human_readable_grad0',hrg,fmt="%s", delimiter=' \t')
