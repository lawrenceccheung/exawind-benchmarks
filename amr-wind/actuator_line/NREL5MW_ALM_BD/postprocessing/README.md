# Postprocessing AMR-Wind results

**Contents**
- [OpenFAST turbine results](openfast-turbine-results)
- [OpenFAST blade loading profiles](openfast-blade-loading-profiles)


The following document describes the post-processing procedures for the AMR-Wind turbine simulation.  

**Note**: In many of the python scripts and Jupyter notebooks provided, the path to the [AMR-Wind frontend](https://github.com/Exawind/amr-wind-frontend) library must be provided.  If necessary, download the library and edit the lines in the python code which define `amrwindfedirs` to include any locations of that library.
```python
# Add any possible locations of amr-wind-frontend here
amrwindfedirs = ['/projects/wind_uq/lcheung/amrwind-frontend/',
                 '/ccs/proj/cfd162/lcheung/amrwind-frontend/']
import sys, os, shutil, io
for x in amrwindfedirs: sys.path.insert(1, x)
```

## OpenFAST turbine results

- Jupyter notebook: [OpenFAST_v40_Results.ipynb](OpenFAST_v40_Results.ipynb)
- python script: [OpenFAST_v40_Results.py](OpenFAST_v40_Results.py)

These scripts extract out specific performance quantities from the OpenFAST output files and creates a time history of quantities to compare, as well as averaging them over a specific time period.  To use the scripts and notebooks above, change the `RUNDIR` variable in the `replacedict` definition:

```python
replacedict={'RUNDIR':'/nscratch/gyalla/HFM/exawind-benchmarks/amr-wind/NREL5MW_ALM_BD/runs/',
             'RESULTSDIR':'../results/OpenFAST_v402_out',
             'RESULTSOLDDIR':'../results/OpenFAST_out'
            }
```

Inside the `yamlstring` variable, also double-check the `trange` variable to make sure the averaging time is correct:

```
trange: &trange [300, 900]   # Note: add 15,000 sec to get AMR-Wind time
```

Then execute and run the notebook/script and it will extract the results.
```bash
$ python OpenFAST_v40_Results.py
```

## OpenFAST blade loading profiles

- Jupyter notebook: [OpenFAST_SectionalLoading.ipynb](OpenFAST_SectionalLoading.ipynb)
- python script: [OpenFAST_SectionalLoading.py](OpenFAST_SectionalLoading.py)

## Contour plots

- Jupyter notebook: []()
- python script: []()

## Averaged wake profiles
