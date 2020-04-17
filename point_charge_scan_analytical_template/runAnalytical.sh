#!/bin/bash

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
   echo 'running position' && echo $i
   mpirun -n 16 $nwchemPath gradInput$i.nw > gradCalc.out
   echo making grad0
   python readForce.py gradCalc.out $xyzFile
   echo moving vectors from $i to $(($i+1))
   cp output.movecs ../pcPosition$(($i+1))/input.movecs
   mpirun -n 4 $nwchemPath  mdInput$i.nw > mdCalc.out &
   cd $home
done
wait
