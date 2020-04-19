# Reads the multi-xyz file from a benzene MD simulation and prints velocities to stdout

import os
import sys
import numpy as np
from pade_powerspec import pade

xyzFile = sys.argv[1]
outFile = 'powerspec.txt'

with open(xyzFile,'r') as f:
        data = f.readlines()

rawVelocities = []
for lineNumber, line in enumerate(data):
	#print (line.split())
	if len(line.split()) == 1:
		molCoords = []
		for mol in range(lineNumber+2,lineNumber+int(line.split()[0])+2):
			molCoords.append(np.asarray(data[mol].split()[4:], dtype=np.float64))
		concatCoords = np.concatenate(molCoords)
		concatCoords = np.insert(concatCoords,0,float(data[lineNumber+1].split()[0]),axis=0)
		#print (concatCoords)
		rawVelocities.append(concatCoords)

		#np.insert(rawVelocities,0,float(data[lineNumber+1].split()[0]))
		if (len(np.concatenate(molCoords))) != 36:
			print (molCoords)
			print (len(molCoords))
			print ('linenumber %s' % lineNumber)
		#print (rawVelocities)
velocities = np.vstack(rawVelocities)
'''
# Create power spectrum from velocities
t = 10*velocities[:,0]
allSpec = 0
for i in range(len(velocities[0,:])):
	x = velocities[:,i]
	w , Fx = pade(t,x)
	allSpec += Fx
np.savetxt(outFile, np.transpose([w,allSpec]))
'''
x = velocities[:,0]
w, Fx = pade(x)
allspec= np.zeros(len(Fx))
for i in range(1,len(velocities[0,:])):
  x = velocities[:,i]
  w, Fx = pade(x)
  allspec = allspec + Fx
np.savetxt('spectrum_ev.txt.pade', np.transpose([w,allspec]))


