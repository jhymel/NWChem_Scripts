Title: Numerical Gradient Calculation Setup and Run Template

This folder contains multiple python scripts for determining the forces applied
to a molecule based on a point charge (-1) placed at (0.0, 0.0, -10.0) (x, y, z)

Explanation of files and scripts:

blankInput - This is a input file for NWChem without any coordinates in its geometry section, this is used as a template to produce all NWChem input files for gradient calculations. (used in inputMaker_new.py)

blankSlurm - This is a slurm run file without any run commands at its end, this is used as a template to produce the run.slurm file. (used in slurmMakerScript.py)

numerical_gradient_estimation.py - This script takes in an xyz file and step size while outputing a file (out) which contains 6n (n=number of atoms) different xyz coordinates for use in determining the gradients in the x,y,z directions.
	Takes two commandline arguments: 
		1. The starting xyz file (look at example.xyz on the github for how this file should be formated)
		2. The step size you wish to use

inputMaker.py - This script takes in the output file from numberical_gradient_estimation.py ('out') and blankInput and uses these to create NwChem input files for each structure in 'out'. These files are named input**.nw (** = integers 0 through the the number of structures in 'out'. These input files are numbered such that each pair (ex. input0.nw, input1.nw ) consists of a single atom shifted forward and backward in the particular axis. For each set of three pairs (ex. (input0.nw, input1.nw), (input2.nw, input3.nw), (input4.nw, input5.nw) ) the first pair corresponds to the x-axis, the second pair corresponds to the y-axis, and the third pair corresponds to the z-axis.
	Takes two commandline arguments:
		1. The output file from numerical_gradient_estimation.py (simply called 'out' by default)
		2. blankInput

slurmMakerScript.py - This script takes in the file blankSlurm and uses it to produce a slurm submission file that contains commands for runnning all NWChem input files in the current directory (any files that that end with .nw). This information is written to a file called 'run.slurm' which can be be run using 'sbatch run.slurm' in commandline.
	Takes in one commandline argument:
		1. blankSlurm

runScript.py - This script takes all .slurm files in the current working directory and submits them to the current cluster's queue.

supraScript.py - This script is the culmination of all the previous entries. It takes in the starting xyz file and step size then calls all the necessary scripts/commands in order to create the gradient estimation files, input files,and slurm files, and then submit slurm files to the queue.
	Takes in two commandline arguements:
		1. The starting xyz file (look at example.xyz on the github for how this file should be formated)
		2. The step size you wish to use

computeGradients.py - This script reads all the output files in pairs (inputX.out, inputX+1.out), uses a grep/awk bash command to retrieve the SCF energy from each calculation, and computes the gradients for each atom using a central finite difference method. This data is then sent to standard out. (An important point, this command is setup so that it when the initialInput.out file is in the current working directory, if that file is not in the current folder then there can be issues with how this program handles the .out files.)
	Takes in one commandline arguement:
		1. The step size you wish to use
