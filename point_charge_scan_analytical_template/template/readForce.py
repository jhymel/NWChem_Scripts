# Title: readForces.py
# Date: 4/17/2020
# This script writes grad0 by parsing lines below particular flags in the output file of a gradient calculation.
# These flags differ depending on if a Hartree-Fork or DFT level of theory is used.

import os
import sys
import commands

home = os.getcwd()
gradientOutputFile = sys.argv[1]
inputGeom = sys.argv[2]

numAtoms = len(open(inputGeom).readlines())

# The below statement checks if the already completed gradient calculation used Hartree-Fock or DFT
if 'scf' == str(commands.getoutput("tail -1 gradInput*.nw")).split(' ')[1].lower():
	start = 0
	with open(readFile,'r') as f:
		for lineNumber, line in enumerate(f):
			if ' '.join(line.split()) == 'RHF ENERGY GRADIENTS':
				start = lineNumber

elif 'dft' == str(commands.getoutput("tail -1 gradInput*.nw")).split(' ')[1].lower():
        start = 0
        with open(readFile,'r') as f:
                for lineNumber, line in enumerate(f):
                        if ' '.join(line.split()) == 'DFT ENERGY GRADIENTS':
                                start = lineNumber

with open(gradientOutputFile,'r') as g:
	with open('grad0','w+') as h:
		buff = g.readlines()
		for i in range(start+4,start+4+numAtoms):
			h.write(buff[i].split()[5] + '\n')
			h.write(buff[i].split()[6] + '\n')
			h.write(buff[i].split()[7] + '\n')
