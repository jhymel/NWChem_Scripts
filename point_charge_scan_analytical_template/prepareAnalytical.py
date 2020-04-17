# Title: prepareAnalytical.py
# Date: 4/16/2020
# This is the primary script for setting up several MD simulations, each based upon an initial perturbation from a single point charge
# that exists only during the first timestep. In this script, initial forces are calculated using NWChem's built-in analytical gradients.
# The number of MD simulations to be run is based upon the number of point charge positions defined in the pcInput file.

# IMPORTANT POINT: Make sure that the last line of the gradInput file is "task scf gradient" or "task dft gradient" (uppercase is fine).
# Either will work, but this is important because the last line of gradInput is checked in order to determine a particular grep call in a later script.

import os
import sys

home = os.getcwd()

#templateFolder = sys.argv[1]
#gradInput = sys.argv[2]
#mdInput = sys.argv[3]
#pcInput = sys.argv[4]
#inputGeom = sys.argv[5]

templateFolder = 'template'
gradInput = 'blankInputGrad'
mdInput = 'blankInputMD'
pcInput = 'pcInput_distance'
inputGeom = 'benzene.xyz'

with open(pcInput,'r') as f:
	for lineNumber, line in enumerate(f):
		# creates a directory for each simulation
		# if directory already exists, then copies over files from template folder
		if os.path.isdir(os.path.join(home,('pcPosition%i' % lineNumber))) == False:
			print('making directory for PC position %i' % lineNumber)
			os.system('cp -r %s pcPosition%i' % (templateFolder,lineNumber))
		else:
			os.system('cp %s/* pcPosition%i' % (templateFolder,lineNumber))
		os.system('cp %s pcPosition%i' % (inputGeom,lineNumber))
		# creates a gradient input file in each directory (by inserting point charge position and geometry information into a gradInput template)
		print('making gradInput%i' % lineNumber)
                with open('pcPosition%i/gradInput%i.nw' % (lineNumber,lineNumber),'w+') as g:
                        with open(gradInput,'r') as k:
                                with open(inputGeom,'r') as h:
                                        for i in k:
                                                if i.split(' ')[0] != 'bq':
                                                        if i.split(' ')[0] != 'geometry':
                                                                g.write(i)
                                                        else:
                                                                g.write(i)
                                                                for atom in h:
                                                                        g.write(atom)
                                                else:
                                                        g.write(i)
                                                        g.write(line)
		# creates MD input file in each directory
		# Future note: Each mdInput*.nw should be identical since the only difference is the gradient/forces file it reads in using read_force
		# Future note: maybe this section could be improved by writing one mdInput file and copying it to each folder?
		print('making mdInput%i' % lineNumber)
		with open('pcPosition%i/mdInput%i.nw' % (lineNumber,lineNumber),'w+') as g:
			with open(mdInput,'r') as k:
				with open(inputGeom,'r') as h:
					for i in k:
                                        	if i.split(' ')[0] != 'geometry':
                                                	g.write(i)
                                        	else:
							g.write(i)
                                                	for atom in h:
                                                        	g.write(atom)
