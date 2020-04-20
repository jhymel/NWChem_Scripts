# Title: point_charge_scan_analytical_template 

# Purpose: Template for building directories for several QMD simulations at once, specifically simulating VEEL spectra for a given XYZ structure using
# forces produced by a point charge perturbation and computed using the analytical gradient machinery in NWChem.

# Important point before starting: In order to run these QMD simulations of VEELS, forces from an initial gradient calculation need to be fed in at the first
# time step of the simulation. This was unable to be done in the standard build of NWChem, therefore certain changes had to be made to the source code (by 6dl).
# So, in order to run this code, you'll need to compile the source code of NWChem on whatever cluster you're on and make the necessary changes outlined in the
# readme in the "modified_qmd_source" directory found in the same Github repo this current file was pulled from.

# Explanation of running process:
# This current directory is meant to be a template that, rather than modifying, should be copied with the name of a particular molecule 
# (i.e. "cp -r point_charge_scan_analytical_template benzene") so that simulations of the molecule are all self-contained within the copied directory.

# In order to produce a VEEL spectrum for a molecule a few steps need to be completed...
	1. Perform a geometry optimization on your molecule of interest at a particular level of theory.
	2. Place that xyz file in this current directory, following the formating of the example file "example_xyz_file".
	3. Modify the "blankInputGrad" and "blankInputMD" NWChem files so that they are using the same level of theory used in the geometry optimization in step 1.
	4. Create an input file containing the charge and coordinates for each point charge you want to examine, following the formating of the example file "example_pcInput_file".
	   Important point: Each point charge (line of the input file) will result in a different QMD simulation being run.
	5. Run the command "python prepareAnalytical.py inputGeom pcInput" (replacing inputGeom and pcInput with the names of your xyz file and point charge input file).
	   This creates directories where each calculation of forces and QMD simulation will be run. Directories are named pcPosition* where * is the line number of pcInput used to generate.
	6. Open queueAnalytical.slurm and make adjustments according to your cluster/resources/NWChem binary location (runAnalytical.sh can also be used in an interactive session).
	7. Batch the slurm file using "sbatch queueAnalytical.slurm" 
	8. Once jobs are complete, QMD output files named mdCalc.out can be found in each pcPosition directory.

