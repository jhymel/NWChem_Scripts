Copy these .F files to $NWCHEM_TOP/src/qmd and compile.

Now, within the qmd input block, add the flag "read_force" to read the components of an external energy gradient (converted internally to force) in to be applied during first step only of MD simulation.  External gradient info should be in a file in the working directory named grad0, and should be structured as follows:

atom1_x
atom1_y
atom1_z
atom2_x
.
.
.
 
