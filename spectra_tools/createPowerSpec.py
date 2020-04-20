# Title: createPowerSpec.py
# Date: 4/20/2020

# This script parses through the multi-xyz file of an QMD simulation for atomic trajectory information at each timestep then uses that
# to produce a power spectrum.

# Important Point:
# The file pade_functions.py must be in the same directory as this when run since the pade_dipole function is called from that file.
# Timestep step size is defined in pade_functions.py and is hard-coded to 10 (since this is the default in NWChem).

import os
import sys
import numpy as np
from pade_functions import pade_power

xyzFile = sys.argv[1]
outFile = 'powerspec.txt'

with open(xyzFile,'r') as f:
        data = f.readlines()

rawVelocities = []
for lineNumber, line in enumerate(data):
	if len(line.split()) == 1:
		molCoords = []
		for mol in range(lineNumber+2,lineNumber+int(line.split()[0])+2):
			molCoords.append(np.asarray(data[mol].split()[4:], dtype=np.float64))
		concatCoords = np.concatenate(molCoords)
		concatCoords = np.insert(concatCoords,0,float(data[lineNumber+1].split()[0]),axis=0)
		rawVelocities.append(concatCoords)

velocities = np.vstack(rawVelocities)

x = velocities[:,0]
w, Fx = pade_power(x)
allspec= np.zeros(len(Fx))
for i in range(1,len(velocities[0,:])):
  x = velocities[:,i]
  w, Fx = pade_power(x)
  allspec = allspec + Fx
np.savetxt(outFile, np.transpose([w,allspec]))
