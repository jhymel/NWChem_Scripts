# Numerical Gradient Estimation

# For a given xyz file, produces additional xyz coordinates
# with each nuclear position is shifted by some arbitrary distance
# in the direction of each axis (x,y,z)

# Usage example:
# Using the script on a xyz file titled 'example.xyz' for a step size of 0.5
# python script.py example.xyz 0.5

import sys

xyzfile = sys.argv[1]
stepSize = float(sys.argv[2])
step_list = [stepSize, stepSize*(-1)]

# Read in coordinates from XYZ file and store as
# list of list of floats (allAtoms)
allAtoms = []
tmpcoords = []
with open(xyzfile, 'r') as f:
    for line in f:
        for coord in range(len(line.split())):
            if coord == 0:
                tmpcoords.append(line.split()[coord])
            else:
                tmpcoords.append(float(line.split()[coord]))
        allAtoms.append(tmpcoords)
        tmpcoords = []
print (allAtoms)

# prints each triplet of starting atomic coordinates followed
# by 6 triplets shifted +/- in the x,y, and z directions

coord_list = []
count = 0
for curAtom in allAtoms:
    #print(str(curAtom) + '\n')
    for curAxis in range(len(allAtoms[0])):
        if curAxis != 0:
            for step in step_list:
                print('#modified atom: %s | axis: %s | step size: %s' % (count,curAxis, step))
                for i in allAtoms:
                    if i !=curAtom:
                        print(i)
                curAtom[curAxis] += step
                print(curAtom)
                curAtom[curAxis] -= step
                print('\n')
        print('\n')
    count += 1

