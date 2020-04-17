#!/bin/bash

module load env/cades-cnms
module load intel/17.0.0
module load intel/openmpi/1.10.4
module load PE-gnu/1.0
source ~/nwchem-6.8/build_env.sh

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
      mpirun $nwchemPath input$j.nw > input$j.out
   done
   echo making grad0
   stepSize=$(sed '3q;d' gradient_estimation.out | awk '{ print $10 }')
   python computeGradients.py $xyzFile $stepSize
   mpirun $nwchemPath mdInput$i.nw > mdCalc.out &
   cd $home
done
wait
