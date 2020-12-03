# NWChem_Scripts
Scripts built for either setting up NWChem inputs or preprocessing for inputs

#### Directories of interest:
- modified_qmd_source
  - Contains Fortran files for compiling the NWChem build needed to run our VEELS QMD simulations 
- point_charge_scan_numerical_template
  - Template for building directories for several QMD simulations at once, specifically simulating VEEL spectra for a given XYZ structure using forces produced by a point charge perturbation and computed using a central finite difference numerical method.
- point_charge_scan_analytical_template
  - Template for building directories for several QMD simulations at once, specifically simulating VEEL spectra for a given XYZ structure using forces produced by a point charge perturbation and computed using the analytical gradient machinery in NWChem.
- spectra_tools
  - Files necessary for creating dipole and power spectra from QMD output files.

### Example of vibrational response from scanning point charges along the C<sub>6</sub> axis of benzene
<img src="VEELS_figure_784.PNG" width="75%"></img> <img src="Benzene_784.gif" width="25%"></img>
<img src="VEELS_figure_1078.png" width="75%"></img> <img src="Benzene_1078.gif" width="25%"></img>
