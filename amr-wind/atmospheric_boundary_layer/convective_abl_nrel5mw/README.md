<!-- This file is automatically compiled into the website. Please copy linked files into .website_src/ paths to enable website rendering -->

# Convectively unstable ABL for wind turbine simulations

This benchmark problem is a slightly convective unstable atmospheric boundary
layer that is used as an inflow for the [actuator line
NREL5MW](../../actuator_line/NREL5MW_ALM_BD/) and geometry resolved NREL5MW
benchmark cases. The conditions and details of the case are sumarized below:

- Hub-height wind speed: 11.4 m/s
- Hub-height wind direction: 240 degrees SW
- Surface roughness: 0.01 m
- Surface temperature flux: 0.005 K-m/s
- Domain size: 5120m x 5120m x 1920m 
- Mesh size: 512 x 512 x 192
- Total mesh size: 50331648 cells

**Contents**

- [Simulation setup](#simulation-setup)
- [Performance](#performance)
- [Results](#results)

## Simulation Setup

Full details of the simulation setup are provided in [**setup documentation**](setup/README.md).

The case was set up using the [AMR-Wind frontend](https://github.com/Exawind/amr-wind-frontend) with the notebook [convectiveABL_setup.ipynb](convective_abl_nrel5mw/setup/convectiveABL_setup.ipynb).  This allows the locations of the refinement regions and sampling planes to be setup properly relative to the location of the NREL5MW turbine.

Input files are in the [input_files](input_files) directory.  There are two stages to this run:

1. Spin-up of the precursor: Use the [convective_abl.inp](input_files/convective_abl.inp) input file to run the case from t=0 to 15,000 seconds.

2. Capture the boundary plane and sampling plane data: Use [convective_abl_bndry.inp](input_files/convective_abl_bndry.inp) to run the case from t=15,000 to 20,000 seconds to output the data needed to run the turbine cases.

Current case was run with AMR-Wind version [f67a52dd6aa1882595d16700527470bc8097cb13](https://github.com/Exawind/amr-wind/commit/f67a52dd6aa1882595d16700527470bc8097cb13)

## Performance

Full details provided in [**performance documentation**](performance/README.md).

The simulation was run on the Sandia Flight HPC cluster using the following resources: 

| Parameter       | Value |
|---              |---  |
| Number of nodes | 8   |
| Number of CPUs  | 896 |
| Wall-time       | 5.4 hours|
| CPU-hours       | 4821.7 |  


## Results

Statistics and results from the ABL are calculated using scripts and notebooks from the [postprocessing](postprocessing) directory, and saved to the [results](directory).  These include quantities such as the:

- Instantaneous hub-height wind speed contours
![HH WS contour](results/XYdomain_15000.png)

- Averaged wind profiles from a virtual metmast at the turbine location
![Met mast average](results/avgmetmast_0600.png)

- Horizontally averaged wind profiles [AVG_horiz_profiles.ipynb](postprocessing/AVG_horiz_profiles.ipynb)

- Time frequency wind spectra [ABLSpectra.ipynb](postprocessing/ABLSpectra.ipynb)
