import os
import sys

inputGeom = sys.argv[1]
stepSize = sys.argv[2]

os.system('python numerical_gradient_estimation.py %s %s > out' % (inputGeom, stepSize))
os.system('python inputMaker.py out blankInput')
os.system('python slurmMakerScript.py blankSlurm')
os.system('python runScript.py')
