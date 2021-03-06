#!/bin/bash

module load env/cades-cnms
module load intel/17.0.0
module load intel/openmpi/1.10.4
module load PE-gnu/1.0
source $NWCHEM_TOP/build_env.sh

# IMPORTANT POINTS: If using xyzFile='*.xyz' only have one xyz file in each pcPosition directory.
# May need to change number of processors in the below mpirun calls depending of what you've requested above

home="$(pwd)"
numberSims=$(find . -name 'pcPosition*' | wc -l)
nwchemPath=$NWCHEM_TOP/bin/LINUX64/nwchem
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
   python computeGradients.py $xyzFile
   mpirun -n 4 $nwchemPath mdInput$i.nw > mdCalc.out &
   cd $home
done
wait
