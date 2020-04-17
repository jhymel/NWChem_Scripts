#!/bin/bash
# Interpreter declaration

#SBATCH -A cnms
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -n 32
#SBATCH -c 1
#SBATCH -J generic_name
#SBATCH --mem=120g
#SBATCH -t 23:59:59
#SBATCH -o ./test-output.txt
#SBATCH -e ./test-error.txt
# sbatch arguments

# Job commands -- this is the same HelloWorld.sh script used in the first example

module load env/cades-cnms
module load intel/17.0.0
module load intel/openmpi/1.10.4
module load PE-gnu/1.0
source ~/nwchem-6.8/build_env.sh

# IMPORTANT POINTS: If using xyzFile='*.xyz' only have one xyz file in each pcPosition directory.
# May need to change number of processors in the below mpirun calls depending of what you've requested above

home="$(pwd)"
numberSims=$(find . -name 'pcPosition*' | wc -l)
nwchemPath='~/nwchem-6.8/bin/LINUX64/nwchem'
xyzFile='*.xyz'

for i in $(seq 0 $(( $numberSims - 1)) )
do
   cd pcPosition$i
   numberInputs=$(find . -name 'input*.nw' | wc -l)
   for j in $(seq 0 $(( $numberInputs - 1)) )
   do
      echo "running position$i input$j"
      mpirun -n 16 $nwchemPath input$j.nw > input$j.out
   done
   echo making grad0
   stepSize=$(sed '3q;d' gradient_estimation.out | awk '{ print $10 }')
   python computeGradients.py $xyzFile $stepSize
   mpirun -n 4 $nwchemPath mdInput$i.nw > mdCalc.out &
   cd $home
done
wait
