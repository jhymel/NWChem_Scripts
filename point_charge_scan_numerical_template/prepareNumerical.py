# Title: prepareNumerical.py
# Date: 4/16/2020
# This is the primary script for setting up several MD simulations, each based upon an initial perturbation from a single point charge.
# The number of MD simulations to be run is based upon the number of point charge positions defined in the pcInput file

import os
import sys

home = os.getcwd()

#templateFolder = sys.argv[1]
#gradInput = sys.argv[2]
#mdInput = sys.argv[3]
#pcInput = sys.argv[4]
#inputGeom = sys.argv[5]
#stepSize = sys.argv[6]

templateFolder = 'template'
gradInput = 'blankInputGrad'
mdInput = 'blankInputMD'
pcInput = 'pcInput_distance'
inputGeom = 'benzene.xyz'
stepSize = 1.0e-5

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
		print('making gradInput%i' % lineNumber)
		# creates a template gradient input file in each directory (since directories are based on point charge position, point charge position is inserted here)
		# coordinates/geometry not inserted here since (number of atoms)*6 gradient input files needed for central finite difference (dealt with in numerical_gradient_estimation.py and inputMaker.py)
		with open('pcPosition%i/gradInput.nw' % (lineNumber),'w+') as g:
			with open(gradInput,'r') as k:
				for i in k:
					if i.split(' ')[0] != 'bq':
						g.write(i)
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
		# once mdInput and template gradInput files are created, the input*.nw files needed for the central finite difference calculation need to be made
		os.chdir('pcPosition%i' % lineNumber)
		print('computing shifted geometries')
		os.system('python numerical_gradient_estimation.py %s %s > gradient_estimation.out' % (inputGeom, stepSize))
		print('making %i run files' % (len(open(inputGeom).readlines())*6))
		os.system('python inputMaker.py gradient_estimation.out gradInput.nw')
		os.chdir(home)
