import os
import sys
#need templateFolder, blankInput, pcInput, stepsize

home = os.getcwd()
pcInput = 'pcInput_distance'

numDirs = len(open(pcInput).readlines())

for folderNumber in range(numDirs):
	print ('opening pcPosition%i' % folderNumber)
	with open('pcPosition%i/mdCalc.out' % (folderNumber),'r') as g:
	#with open('mdCalc.out','r') as g:
		print ('writing timedip for %i' % folderNumber)
		with open('pcPosition%i/timedip' % folderNumber,'w+') as f:
			for line in g:
				if line.split() and line.split()[0] == 'Dipole':
					infoLine = line.split()[3:]
					f.write(' '.join(infoLine)+ '\n')
	print ('building dipoleSpec%i' % folderNumber)
	os.chdir('pcPosition%i' % folderNumber)
	os.system('python spec.py dipoleSpec%i' % (folderNumber))
	os.chdir(home)
			#if line.split()[0] == 'Dipole':
	#	with open(exampleInput,'r') as k:
	#		with open(inputGeom,'r') as h:
	#			for i in k:
	#				if i.split(' ')[0] != 'geometry':
	#					g.write(i)
	#				else:
	#					g.write(i)
	#					for atom in h:
	#						g.write(atom)
	#os.chdir('pcPosition%i' % folderNumber)
	#os.system('python slurmMakerScript.py blankSlurm %s %s' % (inputGeom,nwchemPath))
	#os.chdir(home)
