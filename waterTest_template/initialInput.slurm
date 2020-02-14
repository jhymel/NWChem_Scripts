#!/bin/bash
# Interpreter declaration

#SBATCH -A cnms
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 32
#SBATCH -c 1
#SBATCH -J double_h2o
#SBATCH --mem=120g
#SBATCH -t 10:00
#SBATCH -o ./test-output.txt
#SBATCH -e ./test-error.txt
# sbatch arguments

module load nwchem
module load env/cades-cnms
module load intel/17.0.0
module load intel/openmpi/1.10.4

# Job commands -- this is the same HelloWorld.sh script used in the first example
mpirun nwchem initialInput.nw > initialInput.out
