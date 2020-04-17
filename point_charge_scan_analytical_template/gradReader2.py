import os
import sys
import numpy as np
import random
import matplotlib.pyplot as plt
plt.switch_backend('agg')

home = os.getcwd()
numerical_path = '/home/2h9/benzene/fast_slow_limit/numericalMethod/fine_pc/0_10' 

analytical_folders = [ f for f in os.listdir(home) if os.path.isdir(os.path.join(home,f)) ]
numerical_folders = [ f for f in os.listdir(numerical_path) if os.path.isdir(os.path.join(numerical_path,f)) ]

print (len(analytical_folders))
print (len(numerical_folders))

analytical_folders.sort()
numerical_folders.sort()

magAngleList = []
allList = []

for folder in analytical_folders:
	if os.path.exists(os.path.join(home,folder,'grad0')) and os.path.exists(os.path.join(numerical_path,folder,'grad0')):
		#print ("Yes! It's right here: analytical %s" % folder)
		a_grad = np.loadtxt(os.path.join(home,folder,'grad0'))
		a_grad = np.reshape(a_grad, (-1,3))
		a_norm = np.sum(np.abs(a_grad)**2,axis=-1)**(1./2)
		#print (a_grad)
		#print (a_norm)
	#if os.path.exists(os.path.join(numerical_path,folder,'grad0')):
		#print ("Yes! It's right here: numerical %s" % folder)
		n_grad = np.loadtxt(os.path.join(numerical_path,folder,'grad0'))
		n_grad = np.reshape(n_grad, (-1,3))
		n_norm = np.sum(np.abs(n_grad)**2,axis=-1)**(1./2)
		#print (n_grad)
		#print (n_norm)
		for a_row,n_row in zip(a_grad,n_grad):
		#for a_row,n_row in np.nditer([a_grad[0],n_grad[0]]):
			#print (a_row)
			#print (n_row)
			normalized_a_row = a_row / np.linalg.norm(a_row)
			normalized_n_row = n_row / np.linalg.norm(n_row)
			dot_product = np.dot(normalized_a_row, normalized_n_row)
			angle = np.arccos(dot_product)*57.2958
			mag = np.linalg.norm(a_row) / np.linalg.norm(n_row)
			magAngle = np.array([mag, angle, folder[10:]])
			magAngleList.append(magAngle)
			a_row = np.append(a_row,np.linalg.norm(a_row))
			n_row = np.append(n_row,np.linalg.norm(n_row))
			a_row = np.insert(a_row,0,-1*((float(folder[10:])*0.1)),axis=0)
			n_row = np.insert(n_row,0,-1*((float(folder[10:])*0.1)),axis=0)
			allList.append(np.array([a_row,n_row]))
			#print ("Here's the angle: %f" % angle)
	else:
		print ('something is messed up here: %s' % folder)
#print ('\n')
magAngleList = np.vstack(magAngleList)
#print (allList)
allList = np.vstack(allList)
#print (allList)
analyticalList = allList[::2]
print (max(analyticalList[:,0]))
print (min(analyticalList[:,0]))
numericalList = allList[1::2]
print (max(numericalList[:,0]))
print (min(numericalList[:,0]))
#print (analyticalList)
#print (numericalList)

molLength = len(open(os.path.join(home,'benzene.xyz')).readlines())
analyticalList_a1 = analyticalList[0::12]
analyticalList_a2 = analyticalList[1::12]
analyticalList_a3 = analyticalList[2::12]
analyticalList_a4 = analyticalList[3::12]
analyticalList_a5 = analyticalList[4::12]
analyticalList_a6 = analyticalList[5::12]
analyticalList_a7 = analyticalList[6::12]
analyticalList_a8 = analyticalList[7::12]
analyticalList_a9 = analyticalList[8::12]
analyticalList_a10 = analyticalList[9::12]
analyticalList_a11 = analyticalList[10::12]
analyticalList_a12 = analyticalList[11::12]

np.sort(analyticalList_a1,axis=0)
np.sort(analyticalList_a2,axis=0)
np.sort(analyticalList_a3,axis=0)
np.sort(analyticalList_a4,axis=0)
np.sort(analyticalList_a5,axis=0)
np.sort(analyticalList_a6,axis=0)
np.sort(analyticalList_a7,axis=0) 
np.sort(analyticalList_a8,axis=0) 
np.sort(analyticalList_a9,axis=0) 
np.sort(analyticalList_a10,axis=0)
np.sort(analyticalList_a11,axis=0)
np.sort(analyticalList_a12,axis=0)

#analyticalAtoms = np.array([analyticalList_a1,analyticalList_a2,analyticalList_a3,analyticalList_a4,analyticalList_a5,analyticalList_a6,analyticalList_a7,analyticalList_a8,analyticalList_a9,analyticalList_a10,analyticalList_a11,analyticalList_a12])
analyticalAtoms = np.array([analyticalList_a1,analyticalList_a3,analyticalList_a5,analyticalList_a7,analyticalList_a9,analyticalList_a12])
print (analyticalAtoms)
colors = ['brown', 'red', 'blue', 'purple', 'black', 'green', 'royalblue','indigo', 'orangered', 'navy', 'lawngreen', 'crimson', 'teal', 'springgreen']

fig = plt.figure()
fig.suptitle('Force vs Charge: Slow Limit')
ax = fig.add_subplot(1,1,1)
ax.set_ylabel('|F| (Hartree/Bohr)')
ax.set_xlabel('Fundamental Charge (e-)')
ax.set_xlim(0,-10)
legend = []
atoms = [1, 3, 5, 7, 9, 12]
for i in range(len(analyticalAtoms)):
	x = analyticalAtoms[i][:,0]
	print (max(x))
	print (min(x))
	y = analyticalAtoms[i][:,-1]
	print (max(y))
	print (min(y))
	scatter = ax.scatter(x, y, c=colors[i], s=1)
	legend.append('Atom %s' % atoms[i])

#plt.ylim(0,0.25)
ax.legend(legend,loc='upper left')
ax.set_title('Benzene: Sigma d')
plt.savefig('analytical_benzene_sd.png')

numericalList_a1 = numericalList[0::12]
numericalList_a2 = numericalList[1::12]
numericalList_a3 = numericalList[2::12]
numericalList_a4 = numericalList[3::12]
numericalList_a5 = numericalList[4::12]
numericalList_a6 = numericalList[5::12]
numericalList_a7 = numericalList[6::12]
numericalList_a8 = numericalList[7::12]
numericalList_a9 = numericalList[8::12]
numericalList_a10 = numericalList[9::12]
numericalList_a11 = numericalList[10::12]
numericalList_a12 = numericalList[11::12]

np.sort(numericalList_a1,axis=0) 
np.sort(numericalList_a2,axis=0) 
np.sort(numericalList_a3,axis=0) 
np.sort(numericalList_a4,axis=0) 
np.sort(numericalList_a5,axis=0) 
np.sort(numericalList_a6,axis=0)
np.sort(numericalList_a7,axis=0)
np.sort(numericalList_a8,axis=0)
np.sort(numericalList_a9,axis=0)
np.sort(numericalList_a10,axis=0)
np.sort(numericalList_a11,axis=0)
np.sort(numericalList_a12,axis=0)

#numericalAtoms = np.array([numericalList_a1,numericalList_a2,numericalList_a3,numericalList_a4,numericalList_a5,numericalList_a6,numericalList_a7,numericalList_a8,numericalList_a9,numericalList_a10,numericalList_a11,numericalList_a12])
numericalAtoms = np.array([numericalList_a1,numericalList_a3,numericalList_a5,numericalList_a7,numericalList_a9,numericalList_a12])
print (numericalAtoms)
fig = plt.figure()
fig.suptitle('Force vs Charge: Fast Limit')
ax = fig.add_subplot(1,1,1)
ax.set_ylabel('|F| (Hartree/Bohr)')
ax.set_xlabel('Fundamental Charge (e-)')
ax.set_xlim(0,-10)
for i in range(len(numericalAtoms)):
	x = numericalAtoms[i][:,0]
	print (max(x))
	print (min(x))
	y = numericalAtoms[i][:,-1]
	print (max(y))
	print (min(y))
	ax.scatter(x, y, c=colors[i], s=1)
#plt.ylim(0,0.25)

ax.set_title('Benzene: Sigma d')
ax.legend(legend,loc='upper left')
plt.savefig('numerical_benzene_sd.png')

#print (magAngleList.tolist())
#print (allList.tolist())
#np.savetxt('magAngle_benzene.csv', magAngleList, delimiter=',', fmt="%s")
#np.savetxt('allList_benzene.csv', allList, delimiter=',')
#np.savetxt('analyticalAtoms.csv',analyticalAtoms,delimiter=',')
#print (folders)
