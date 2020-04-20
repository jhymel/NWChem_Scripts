# Title: createDipoleSpec.py
# Date: 4/20/2020

# This script parses through the output file of an QMD simulation for dipole information at each timestep then uses that
# to produce an IR spectrum.

# Important Point:
# The file pade_functions.py must be in the same directory as this when run since the pade_dipole function is called from that file.
# Timestep step size is defined in pade_functions.py and is hard-coded to 10 (since this is the default in NWChem).

import os
import sys
import numpy as np
from pade_functions import pade_dipole

# This read file is the ouput of a QMD simulation, typically named mdCalc.out and found in pcPosition* directories
readFile = sys.argv[1]
outFile = 'dipolespec.txt'

with open(readFile,'r') as f:
        data = f.readlines()

dipoles = []
for lineNumber, line in enumerate(data):
        if 'Dipole (' in line:
                dipoles.append(np.asarray(line.split()[-4:], dtype=np.float64))

dipoles = np.vstack(dipoles)

t = dipoles[:,0]
x = dipoles[:,1]
y = dipoles[:,2]
z = dipoles[:,3]
w, Fx      = pade_dipole(t,x)
w, Fy      = pade_dipole(t,y)
w, Fz      = pade_dipole(t,z)

np.savetxt(outFile, np.transpose([w,Fx+Fx+Fz]))
